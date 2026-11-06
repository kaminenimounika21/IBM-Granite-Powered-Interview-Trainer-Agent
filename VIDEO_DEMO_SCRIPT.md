# 2–3 Minute Project Demonstration Video Script
## IBM Granite-Powered Interview Trainer Agent
### Problem Statement No. 22 • IBM SkillsBuild University Education Project

---

### Video Overview
- **Target Duration:** 2 minutes 45 seconds
- **Tone:** Professional, engaging, confident, and clear
- **Presenter Setup:** Screen recording with web browser running `http://localhost:8000`, voiceover narration, and optional webcam picture-in-picture.

---

### Step-by-Step Script & Visual Storyboard

#### [0:00 - 0:25] Scene 1: Introduction & The Core Problem
- **Visual:** Browser opens to the Welcome Page (`welcome-view`). The camera focuses on the IBM Carbon header, the "SkillsBuild 2026" badge, and the active "IBM Granite 3.0 Active" status chip.
- **Narrator (Voiceover):**
  > "Hello everyone! Welcome to our demonstration of the **IBM Granite-Powered Interview Trainer Agent**, developed for Problem Statement No. 22 in the IBM SkillsBuild University Project.
  > 
  > Every year, millions of engineering students and professionals struggle to prepare effectively for competitive technical interviews. Standard practice platforms offer only static problem lists, lack personalized feedback on resumes, and leave candidates unprepared for behavioral STAR questions.
  > 
  > Our solution addresses this challenge by combining **IBM Granite 3.0**, **IBM Docling**, **IBM Langflow**, and **IBM watsonx.ai** into an intelligent, personalized interview coach."

---

#### [0:25 - 0:55] Scene 2: Candidate Profiling & IBM Docling Resume Intelligence
- **Visual:** Presenter clicks **"Resume Upload"** in the sidebar. Chooses `sample_resume.txt`, selects "Cloud Application Developer", and clicks **"Upload & Parse with IBM Docling"**. The screen transitions smoothly to the **Resume Analysis** view.
- **Narrator (Voiceover):**
  > "Let's begin with candidate intelligence. We upload a candidate's resume. Behind the scenes, **IBM Docling Core** parses the document into a structured layout tree, extracting skills, education, and projects.
  > 
  > Immediately, we see the results: IBM Docling identified 17 technical skills—including Python, Docker, SQL, and FastAPI—and benchmarked them against the target Cloud Developer role. It detected missing prerequisite skills, like Kubernetes and Microservices, and calculated an objective Profile Readiness Score of 98/100, alongside structured Docling Markdown."

---

#### [0:55 - 1:30] Scene 3: RAG Knowledge Retrieval & IBM Granite Question Generation
- **Visual:** Presenter navigates to **"AI Question Generator"**. Selects "Cloud Application Developer", "Mixed", and "5 Questions", then clicks **"Generate Questions with IBM Granite"**. The questions appear with category tags, difficulty badges, and RAG source citations.
- **Narrator (Voiceover):**
  > "Next, let's generate grounded interview questions. Powered by **IBM Langflow** and **IBM Slate dense embeddings**, our RAG pipeline retrieves relevant technical and behavioral knowledge from our curated IBM repository.
  > 
  > **IBM Granite 3.0** then synthesizes personalized questions across four tracks: Technical, HR, Behavioral, and Scenario-based. Notice how each question comes with explicit evaluation criteria, follow-up concepts, interview tips, and complete model answers grounded in source documents."

---

#### [1:30 - 2:05] Scene 4: Interactive Mock Interview with Voice Recognition
- **Visual:** Presenter navigates to **"Interactive Mock Interview"**, clicks **"Begin Mock Interview Session"**. Question 1 appears with a running countdown timer. Presenter clicks the **"🎙 Speak Your Answer"** button, speaks a sample answer, and text appears in real time. Presenter clicks **"Submit Answer for AI Evaluation"**.
- **Narrator (Voiceover):**
  > "Now, the flagship experience: the **Interactive Mock Interview**. Candidates can practice under realistic timed conditions.
  > 
  > Using browser speech recognition, candidates can speak their responses out loud:
  > *'I design stateless microservices using Docker containers and implement circuit breakers for fault tolerance.'*
  > 
  > Upon submission, **IBM Granite** evaluates the answer across six objective criteria: Technical Correctness, Relevance, Clarity, Communication, Completeness, and Problem Solving. Candidates receive an instant score breakdown, key strengths, improvement areas, and an enhanced model answer."

---

#### [2:05 - 2:30] Scene 5: Adaptive 7-Day Roadmap & Real-Time Dashboard
- **Visual:** Presenter clicks **"Preparation Roadmap"** in the sidebar, displaying the 7-day schedule, then transitions to the **"Interview Preparation Dashboard"** showing updated progress indicators, mock scores, and skill gap cards.
- **Narrator (Voiceover):**
  > "To ensure continuous improvement, the agent automatically synthesizes a **Personalized 7-Day Preparation Roadmap** tailored to the candidate's diagnosed skill gaps, with daily technical tasks, STAR behavioral prompts, and recommended IBM SkillsBuild learning modules.
  > 
  > Everything synchronizes with our **Candidate Dashboard**, displaying real calculated metrics, strong skills, and measurable practice progress."

---

#### [2:30 - 2:45] Scene 6: Conclusion & IBM Cloud Deployment
- **Visual:** Presenter clicks **"Application Settings"** showing live watsonx.ai model status and connection test, then briefly switches to terminal showing `tests/test_all.py` passing 15/15 tests.
- **Narrator (Voiceover):**
  > "The entire application is 100% functional, containerized for **IBM Cloud Code Engine**, fully compatible with the IBM Cloud Lite tier, and backed by a comprehensive 15-module automated test suite.
  > 
  > Thank you for watching, and thank you to the IBM SkillsBuild team for this incredible opportunity!"
- **Visual:** End card with Project Title, Team details, and IBM SkillsBuild 2026 logo.
