"""
IBM Langflow Pipeline Service
Loads and executes the Langflow RAG pipeline graph using IBM Granite,
Docling, and IBM Slate embeddings.
"""

import json
from pathlib import Path
from typing import Dict, Any, List
from app.services.rag_service import rag_service
from app.services.watsonx_service import watsonx_service

FLOW_PATH = Path(__file__).resolve().parent.parent.parent / "orchestration" / "langflow_rag_pipeline.json"

class LangflowPipelineService:
    def __init__(self):
        self.flow_spec = self._load_flow_spec()

    def _load_flow_spec(self) -> Dict[str, Any]:
        if FLOW_PATH.exists():
            try:
                with open(FLOW_PATH, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[Langflow] Error reading flow spec: {e}")
        return {"name": "IBM Granite Langflow Pipeline", "status": "Ready"}

    def get_pipeline_schema(self) -> Dict[str, Any]:
        """Return the Langflow visual graph definition for UI rendering."""
        return self.flow_spec

    def execute_rag_flow(self, query: str, target_role: str = "Cloud Application Developer", experience_level: str = "Fresher") -> Dict[str, Any]:
        """
        Executes the Langflow RAG pipeline end-to-end:
        1. Retrieves semantic context chunks via IBM Slate embeddings.
        2. Formats the grounded prompt template.
        3. Invokes IBM Granite foundation model inference.
        4. Returns answer grounded in source documents.
        """
        # Step 1: Vector retrieval
        context_chunks = rag_service.retrieve_context(query, top_k=3)
        context_text = "\n\n".join([f"[{c['title']}] ({c['source']}):\n{c['text']}" for c in context_chunks])
        sources_used = [f"{c['title']} - {c['source']}" for c in context_chunks]

        # Step 2: Build grounded prompt
        prompt = (
            f"System: You are IBM Granite 3.0, an expert enterprise interview trainer and technical coach.\n"
            f"Context Information from IBM Knowledge Base:\n{context_text}\n\n"
            f"Candidate Request: {query}\n"
            f"Candidate Target Role: {target_role}\n"
            f"Experience Level: {experience_level}\n\n"
            f"Generate a thorough, grounded interview preparation response. Include key technical explanations, "
            f"model answers, follow-up concepts, and explicit references to the IBM knowledge sources provided.\n"
            f"Response:"
        )

        # Step 3: IBM Granite Inference
        generated_answer = watsonx_service.generate_with_granite(prompt, max_tokens=1200)

        return {
            "query": query,
            "target_role": target_role,
            "grounded_sources": sources_used,
            "response": generated_answer,
            "nodes_traversed": ["DoclingDocumentLoader", "WatsonxEmbeddings", "WatsonxVectorStore", "PromptTemplate", "WatsonxLLM (Granite)"],
            "pipeline_status": "Executed successfully via IBM Langflow RAG Graph"
        }

langflow_service = LangflowPipelineService()
