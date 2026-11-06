# User Guide: IBM Granite Interview Trainer Agent

## Quickstart, Configuration & Operational Guide

---

### 1. Prerequisites
- Python 3.10+
- Modern Web Browser (Chrome, Firefox, Edge, Safari) with microphone access for speech recognition.
- (Optional) IBM Cloud Account with watsonx.ai instance for live cloud inference.

---

### 2. Local Installation & Launch

#### Step 1: Clone or Navigate to the Workspace
```powershell
cd c:\IBM
```

#### Step 2: Install Dependencies
```powershell
python3 -m pip install -r requirements.txt
```

#### Step 3: Run the Application
```powershell
python3 run.py
```
The server will start at: `http://localhost:8000`

---

### 3. IBM Cloud Credentials Configuration

The application is fully operational out-of-the-box with IBM Granite structured prompt templates, IBM Docling Core document parsing, and IBM Slate vector embeddings.

To connect directly to your live **IBM Cloud watsonx.ai** instance:

#### Option A: Via the Web UI (Application Settings Page)
1. Navigate to **"15. Application Settings"** in the sidebar.
2. Enter your **IBM Cloud API Key** (from [IBM Cloud IAM Keys](https://cloud.ibm.com/iam/apikeys)).
3. Enter your **watsonx.ai Project ID** (from your watsonx.ai Project Settings GUID).
4. Select your preferred Granite model (e.g. `ibm/granite-3-8b-instruct`).
5. Click **"Save Settings & Persist to .env"**.
6. Click **"Test Live watsonx.ai Connection"** to verify immediate connectivity!

#### Option B: Via `.env` File
Create a `.env` file in the project root:
```env
WATSONX_APIKEY=your_ibm_cloud_api_key_here
WATSONX_PROJECT_ID=your_watsonx_project_guid_here
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_MODEL_ID=ibm/granite-3-8b-instruct
WATSONX_EMBEDDING_MODEL_ID=ibm/slate-30m-english-rtr
```

---

### 4. Running the Automated Test Suite

A comprehensive 15-module automated test suite is provided to verify all core functional requirements:

```powershell
python3 tests/test_all.py
```

Expected output:
```
Ran 15 tests in 0.580s
OK
[PASS] Test 1: System status correctly reports full IBM technology stack.
[PASS] Test 2: Candidate registration and login succeeded.
[PASS] Test 3: Profile saved and retrieved correctly.
[PASS] Test 4: IBM Docling parsed resume. Detected 17 skills. Readiness: 98/100.
[PASS] Test 5: Skill gap identification successful. Missing skills: ['Rest Api', 'Kubernetes'].
[PASS] Test 6: Job role selection and calibration active.
[PASS] Test 7: RAG semantic retrieval verified. Top chunk: 'ACID Properties & Transaction Isolation Levels'.
[PASS] Test 8: IBM Granite generated 3 grounded questions.
[PASS] Test 9: Comprehensive model answer and criteria verified.
[PASS] Test 10: Mock interview session started, answer submitted, and evaluated.
[PASS] Test 11: Answer evaluated across all 6 criteria. Overall score: 60/100.
[PASS] Test 12: 7-Day personalized preparation roadmap generated successfully.
[PASS] Test 13: Dashboard metrics computed: Progress=39%, AvgScore=75.0%.
[PASS] Test 14: Short/invalid input handled gracefully with constructive coaching.
[PASS] Test 15: Frontend Single-Page Portal and IBM Carbon CSS/JS verified.
```

---

### 5. Step-by-Step User Walkthrough (15 Application Pages)

1. **Welcome & Overview (`#welcome-view`):** Executive summary, target user pathways, and technology stack overview.
2. **Registration & Login (`#auth-view`):** Candidate sign-in and account initialization.
3. **Candidate Dashboard (`#dashboard-view`):** Visual progress bar, mock scores, strong skills vs. skill gaps, and next activities.
4. **Candidate Profile (`#profile-view`):** Comprehensive interview preparation form collecting education, college, target role, technical skills, languages, and preferred company.
5. **Resume Upload (`#resume-upload-view`):** Accepts PDF, DOCX, and TXT resumes; uploads securely and triggers IBM Docling.
6. **Resume Analysis (`#resume-analysis-view`):** Displays extracted skills, detected gaps, education summary, project highlights, readiness score, and IBM Docling Markdown representation.
7. **Target Job Roles (`#job-role-view`):** One-click track calibration for Cloud Developer, AI/RAG Engineer, Backend Engineer, and Campus Placement Freshers.
8. **AI Question Generator (`#question-generator-view`):** Generates personalized, RAG-grounded questions across Technical, HR, Behavioral, and Scenario tracks.
9. **Model Answers & Explanations (`#model-answers-view`):** Explores benchmark answers, evaluation criteria, and tips.
10. **Interactive Mock Interview (`#mock-interview-view`):** Stepper workflow with running timer, browser speech-to-text voice input, inline AI evaluation, and summary report.
11. **Answer Evaluation (`#answer-eval-view`):** Standalone analysis of any candidate response across 6 objective criteria with beginner-friendly alternative phrasing.
12. **Preparation Roadmap (`#roadmap-view`):** 7-day structured schedule with daily technical tasks, STAR behavioral prompts, and recommended IBM SkillsBuild learning modules.
13. **Practice History (`#history-view`):** Historical logs of all answered questions and completed mock interview scores.
14. **Knowledge Base Management (`#kb-management-view`):** Inspect indexed chunks, dense embeddings, and add custom interview documents.
15. **Application Settings (`#settings-view`):** Configure watsonx.ai credentials, model selection, IBM COS bucket endpoints, and test live connection.

---

### 6. IBM Cloud Deployment Guide

#### Step 1: Install IBM Cloud CLI
Download and install `ibmcloud` CLI from [cloud.ibm.com/docs/cli](https://cloud.ibm.com/docs/cli).

#### Step 2: Login to IBM Cloud
```bash
ibmcloud login -a cloud.ibm.com -r us-south -g Default
```

#### Step 3: Deploy to IBM Cloud Code Engine
Execute the automated deployment script:
```powershell
deploy\deploy-ibm-cloud.bat
```
Or execute manually:
```bash
# Target Code Engine project
ibmcloud ce project select --name ibm-skillsbuild-project

# Deploy application from local source or container registry
ibmcloud ce app create --name ibm-granite-trainer \
  --build-source . \
  --port 8000 \
  --min-scale 0 \
  --max-scale 1 \
  --cpu 0.25 \
  --memory 0.5G \
  --env WATSONX_URL=https://us-south.ml.cloud.ibm.com \
  --env WATSONX_MODEL_ID=ibm/granite-3-8b-instruct \
  --env WATSONX_APIKEY=YOUR_IBM_API_KEY \
  --env WATSONX_PROJECT_ID=YOUR_PROJECT_ID
```
Code Engine will build the container, provision the serverless pod, scale down to zero when idle (complying with IBM Cloud Lite free tier quotas), and output your public URL (e.g. `https://ibm-granite-trainer.us-south.codeengine.appdomain.cloud`).
