# IBM Granite-Powered Interview Trainer Agent
### Problem Statement No. 22 • IBM SkillsBuild University Education Project 2026

[![IBM watsonx.ai](https://img.shields.io/badge/IBM%20watsonx.ai-Granite%203.0-0f62fe?logo=ibm)](https://www.ibm.com/products/watsonx-ai)
[![IBM Docling](https://img.shields.io/badge/IBM%20Docling-Core%202.106.0-0043ce?logo=ibm)](https://github.com/DS4SD/docling)
[![IBM Langflow](https://img.shields.io/badge/IBM%20Langflow-RAG%20Pipeline-8a3ffc?logo=ibm)](https://www.ibm.com)
[![IBM Cloud Code Engine](https://img.shields.io/badge/IBM%20Cloud-Code%20Engine-24a148?logo=ibm)](https://cloud.ibm.com/codeengine)
[![Tests Passing](https://img.shields.io/badge/Tests-15%2F15%20Passing-success)](tests/test_all.py)

---

## 1. Project Overview

The **IBM Granite-Powered Interview Trainer Agent** is a full-stack, enterprise-grade AI coaching application built strictly using **IBM Cloud** technologies and foundation models. It prepares students, freshers, and experienced professionals for competitive engineering interviews through:

- **Resume Intelligence with IBM Docling:** Parses PDF, DOCX, and text resumes into structural layout trees, extracts candidate skills, and benchmarks them against industry target roles to detect missing competencies.
- **RAG-Powered Grounded Knowledge with IBM Langflow:** Retrieves domain knowledge across Technical (DSA, Cloud, DBMS, OS, Networks), HR, and Behavioral tracks using **IBM Slate dense embeddings** (`ibm/slate-30m-english-rtr`) to prevent hallucinations.
- **Foundation Model Reasoning with IBM Granite 3.0:** Generates personalized questions across Technical, HR, Behavioral (STAR), and Scenario-based categories with full model answers, follow-ups, and tips.
- **Interactive Mock Interview Simulation:** Conducts timed interview sessions with real-time browser speech recognition (voice-to-text) and granular 6-criterion evaluation.
- **Adaptive 7-Day Roadmaps:** Synthesizes custom daily learning schedules tailored to the candidate's diagnosed skill gaps and links directly to IBM SkillsBuild learning modules.

---

## 2. Strict Technology Mapping

In strict compliance with project requirements, only IBM technologies are utilized:

| Capability | IBM Technology Integrated | Implementation / Package |
| :--- | :--- | :--- |
| **Foundation Model** | **IBM Granite 3.0** (`ibm/granite-3-8b-instruct`) | `ibm-watsonx-ai` SDK & Granite prompt synthesis |
| **AI Inference Platform** | **IBM watsonx.ai** | IAM Bearer Token & watsonx REST / SDK |
| **Document Intelligence** | **IBM Docling Core** (v2.106.0) | `docling_core.types.doc.DoclingDocument` |
| **Dense Vector Embeddings** | **IBM Slate** (`ibm/slate-30m-english-rtr`) | 384-dimensional dense semantic vector retrieval |
| **RAG Pipeline Orchestrator**| **IBM Langflow** | `orchestration/langflow_rag_pipeline.json` graph |
| **Agent Orchestration** | **IBM watsonx Orchestrate** | OpenAPI 3.0 Agent Skill Specification |
| **Document Vault** | **IBM Cloud Object Storage (COS)** | `ibm_boto3` SDK & secure partition vault |
| **Application Hosting** | **IBM Cloud Code Engine** | Red Hat UBI 9 Dockerfile & deployment manifests |
| **UI Design System** | **IBM Carbon Design System** | Custom CSS/JS adhering to Carbon palette & fonts |

---

## 3. System Architecture

```
Layer 1: User Interface (IBM Carbon Design System, 15 SPA Views, Web Speech Audio)
                   │
Layer 2: Document Processing (IBM Docling Core - Resume Hierarchy & Skill Gaps)
                   │
Layer 3: Retrieval & Knowledge (IBM Langflow & IBM Slate Dense Embeddings RAG)
                   │
Layer 4: AI Foundation Intelligence (IBM Granite 3.0 via watsonx.ai)
                   │
Layer 5: Agent Orchestration (IBM watsonx Orchestrate Multi-Step Coordinator)
                   │
Layer 6: IBM Cloud Infrastructure (IBM Code Engine, IBM Cloud Object Storage, IAM)
```

---

## 4. 15 Application Pages

The application provides a seamless Single-Page Application (SPA) experience across 15 distinct functional views:

1. **Welcome / Home Page:** Executive overview, user paths, and technology stack.
2. **Candidate Registration & Login:** Candidate account management and persistent profile tracking.
3. **Candidate Profile:** Comprehensive interview preferences form (experience, education, skills, target role).
4. **Resume Upload:** Document ingestion supporting PDF, DOCX, and TXT with candidate privacy.
5. **Resume Analysis:** IBM Docling layout extraction, skill tags, gap analysis, and readiness score (0-100).
6. **Interview Preparation Dashboard:** Real calculated statistics, progress meter, strong skills vs. gaps.
7. **Job Role Selection:** One-click track switching (Cloud Developer, AI/RAG Engineer, Backend, Campus Fresher).
8. **AI Interview Question Generator:** Granite-generated questions with difficulty levels and RAG citations.
9. **Model Answers and Explanations:** Comprehensive benchmark answers, trade-off explanations, and tips.
10. **Interactive Mock Interview:** Question stepper with countdown timer and voice-to-text audio input.
11. **Answer Evaluation:** Detailed breakdown across 6 objective criteria with model improvements.
12. **Personalized Preparation Roadmap:** Tailored 7-day learning schedule with IBM SkillsBuild links.
13. **Practice History:** Persistent logs of answered questions and completed mock interview scores.
14. **Knowledge Base Management:** RAG chunk browser, IBM Slate embedding inspector, and custom document indexer.
15. **Application Settings:** Live watsonx.ai connection testing, model selection, and API credentials management.

---

## 5. Quickstart & Running Locally

### Step 1: Install Dependencies
```powershell
python3 -m pip install -r requirements.txt
```

### Step 2: Run Application Server
```powershell
python3 run.py
```
Open your browser at: **`http://localhost:8000`**

### Step 3: Run Automated Test Suite
```powershell
python3 tests/test_all.py
```
*All 15 automated test cases run and pass in ~0.6 seconds!*

---

## 6. Project Directory Structure

```
c:\IBM\
├── app\
│   ├── __init__.py
│   ├── main.py                     # FastAPI application & route registry (15 pages & APIs)
│   ├── config.py                   # IBM Cloud credentials & runtime settings
│   ├── database.py                 # Persistent SQLite storage with Cloudant adapter
│   ├── services\
│   │   ├── __init__.py
│   │   ├── watsonx_service.py      # IBM watsonx.ai SDK, Granite inference, Slate embeddings
│   │   ├── docling_service.py      # IBM Docling Core 2.106.0 document parsing & skill gaps
│   │   ├── rag_service.py          # RAG pipeline with IBM Slate embeddings & cosine retrieval
│   │   ├── langflow_pipeline.py    # IBM Langflow pipeline runner & schema provider
│   │   ├── orchestrate_service.py  # Agent workflow coordinator (Questions, Eval, Roadmap)
│   │   └── cos_service.py          # IBM Cloud Object Storage vault adapter (ibm_boto3)
│   ├── data\
│   │   └── knowledge_base\         # 8 authoritative knowledge domain files
│   ├── schemas\
│   │   └── models.py               # Pydantic data schemas
│   ├── static\
│   │   ├── css\carbon_theme.css    # IBM Carbon Design System styling
│   │   └── js\app.js               # Client controller, 15-view router, speech recognition
│   └── templates\
│       └── index.html              # Comprehensive Carbon SPA portal
├── tests\
│   ├── test_all.py                 # Automated verification test suite (15 tests)
│   └── sample_resume.txt           # Sample test resume
├── orchestration\
│   ├── orchestrate_skill_spec.json # IBM watsonx Orchestrate OpenAPI skill spec
│   └── langflow_rag_pipeline.json  # IBM Langflow RAG visual workflow graph
├── deploy\
│   ├── Dockerfile                  # Red Hat UBI 9 container definition
│   ├── deployment.yaml             # Kubernetes / Code Engine manifest
│   ├── manifest.yml                # IBM Cloud Foundry / Code Engine manifest
│   └── deploy-ibm-cloud.bat        # Automated IBM Cloud deployment script
├── docs\
│   ├── PROBLEM_STATEMENT.md        # Problem Statement No. 22 & impact analysis
│   ├── SYSTEM_ARCHITECTURE.md      # 6-layer architecture with Mermaid diagram
│   ├── PRESENTATION_OUTLINE.md     # 15-slide PowerPoint deck outline
│   ├── VIDEO_DEMO_SCRIPT.md        # 2-3 minute project demonstration video script
│   └── USER_GUIDE.md               # User guide & deployment instructions
├── .env.example                    # Template for IBM credentials
├── requirements.txt                # Python package dependencies
├── run.py                          # Application startup launcher
└── README.md                       # Master project documentation
```

---

## 7. SkillsBuild Project Submission Deliverables

Complete deliverables required by the **IBM SkillsBuild University Education Project Guidelines**:
- **Problem Statement Analysis:** Located at [`docs/PROBLEM_STATEMENT.md`](docs/PROBLEM_STATEMENT.md)
- **Architectural Diagram & Layer Mapping:** Located at [`docs/SYSTEM_ARCHITECTURE.md`](docs/SYSTEM_ARCHITECTURE.md)
- **PowerPoint Presentation Outline (15 Slides):** Located at [`docs/PRESENTATION_OUTLINE.md`](docs/PRESENTATION_OUTLINE.md)
- **2–3 Minute Demonstration Video Script:** Located at [`docs/VIDEO_DEMO_SCRIPT.md`](docs/VIDEO_DEMO_SCRIPT.md)
- **Operational User Guide:** Located at [`docs/USER_GUIDE.md`](docs/USER_GUIDE.md)

---

## 8. Responsible AI & Ethical Standards

This application complies with IBM's Trust & Transparency principles:
- **Fairness & Constructive Coaching:** AI scores assess preparation quality, not innate intelligence or employment guarantees.
- **Explainability:** Every score is broken down across 6 criteria with explicit rationales and beginner-friendly alternatives.
- **Privacy & Security:** Resumes are vaulted securely in private partitions; user information is never shared or leaked.
- **Anti-Hallucination:** Grounded in authoritative RAG documentation via IBM Slate embeddings before IBM Granite synthesis.
