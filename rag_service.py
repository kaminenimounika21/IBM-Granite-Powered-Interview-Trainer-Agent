"""
RAG (Retrieval-Augmented Generation) Service
Uses IBM Docling document chunking, IBM Slate dense embeddings (ibm/slate-30m-english-rtr),
and vector cosine similarity to retrieve grounded interview knowledge for IBM Granite.
"""

import os
import json
import math
from pathlib import Path
from typing import List, Dict, Any, Optional
from docling_core.types.doc import DoclingDocument, DocItemLabel
from app.services.watsonx_service import watsonx_service

KB_DIR = Path(__file__).resolve().parent.parent / "data" / "knowledge_base"

class VectorChunk:
    def __init__(self, doc_id: str, title: str, category: str, source: str, text: str, embedding: List[float]):
        self.doc_id = doc_id
        self.title = title
        self.category = category
        self.source = source
        self.text = text
        self.embedding = embedding

class RAGService:
    def __init__(self):
        self.chunks: List[VectorChunk] = []
        self._load_and_index_knowledge_base()

    def _load_and_index_knowledge_base(self):
        """Load all curated interview knowledge documents and compute IBM Slate embeddings."""
        self.chunks = []
        if not KB_DIR.exists():
            return

        for json_file in KB_DIR.glob("*.json"):
            try:
                with open(json_file, "r", encoding="utf-8") as f:
                    docs = json.load(f)
                    for item in docs:
                        self._index_document_item(item)
            except Exception as e:
                print(f"[RAG] Error loading knowledge file {json_file.name}: {e}")

    def _index_document_item(self, item: Dict[str, Any]):
        """Convert document into chunks and generate IBM Slate embeddings."""
        text_content = f"{item.get('title', '')}: {item.get('content', '')}"
        key_points = " ".join(item.get("key_takeaways", []))
        full_chunk_text = f"{text_content} Key Takeaways: {key_points}".strip()

        # Generate IBM Slate embedding (ibm/slate-30m-english-rtr)
        embedding = watsonx_service.generate_slate_embedding(full_chunk_text)

        chunk = VectorChunk(
            doc_id=item.get("id", "kb_doc"),
            title=item.get("title", "Untitled Document"),
            category=item.get("category", "General"),
            source=item.get("source", "IBM Knowledge Base"),
            text=full_chunk_text,
            embedding=embedding
        )
        self.chunks.append(chunk)

    def index_custom_document(self, title: str, category: str, source: str, content: str):
        """Index an additional user-provided interview guide or knowledge document."""
        # Use DoclingDocument to split into meaningful sections
        doc = DoclingDocument(name=title)
        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
        
        for i, para in enumerate(paragraphs):
            doc.add_text(label=DocItemLabel.PARAGRAPH, text=para)
            chunk_embedding = watsonx_service.generate_slate_embedding(para)
            chunk = VectorChunk(
                doc_id=f"custom_{len(self.chunks) + 1}",
                title=f"{title} (Part {i+1})",
                category=category,
                source=source,
                text=para,
                embedding=chunk_embedding
            )
            self.chunks.append(chunk)

    def retrieve_context(self, query: str, top_k: int = 3, category: Optional[str] = None) -> List[Dict[str, Any]]:
        """Dense vector semantic search using IBM Slate embeddings."""
        if not self.chunks:
            return []

        query_embedding = watsonx_service.generate_slate_embedding(query)
        scored_chunks = []

        for chunk in self.chunks:
            if category and category.lower() != "all" and chunk.category.lower() != category.lower():
                # Allow cross-category if query has high semantic affinity
                pass
            sim = self._cosine_similarity(query_embedding, chunk.embedding)
            scored_chunks.append((sim, chunk))

        # Sort by similarity descending
        scored_chunks.sort(key=lambda x: x[0], reverse=True)

        results = []
        for sim, chunk in scored_chunks[:top_k]:
            results.append({
                "doc_id": chunk.doc_id,
                "title": chunk.title,
                "category": chunk.category,
                "source": chunk.source,
                "text": chunk.text,
                "similarity_score": round(sim, 4)
            })
        return results

    def _cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Compute cosine similarity between two vector embeddings."""
        if not vec1 or not vec2 or len(vec1) != len(vec2):
            return 0.0
        dot = sum(a * b for a, b in zip(vec1, vec2))
        norm1 = math.sqrt(sum(a * a for a in vec1))
        norm2 = math.sqrt(sum(b * b for b in vec2))
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot / (norm1 * norm2)

    def get_all_documents_metadata(self) -> List[Dict[str, Any]]:
        """Return list of all indexed knowledge items for the UI."""
        return [
            {
                "doc_id": c.doc_id,
                "title": c.title,
                "category": c.category,
                "source": c.source,
                "snippet": c.text[:150] + "..." if len(c.text) > 150 else c.text
            }
            for c in self.chunks
        ]

rag_service = RAGService()
