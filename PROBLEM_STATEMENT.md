# Problem Statement No. 22: IBM Granite-Powered Interview Trainer Agent

## IBM SkillsBuild University Education Project 2026

---

### 1. Executive Summary & Industry Problem

The tech hiring ecosystem faces a massive preparation gap. Every year, millions of computer science students, engineering graduates, and transitioning professionals apply for high-impact software, cloud, and AI engineering roles. However, traditional interview preparation suffers from systemic limitations:

1. **Generic, Static Question Banks:** Standard online platforms offer static lists of coding problems that lack personalization, realistic conversational back-and-forth, or alignment with specific enterprise roles and candidate resumes.
2. **Disconnected Resume Benchmarking:** Candidates rarely know their specific skill gaps against a job description until they are rejected. Resumes are parsed by hiring ATS algorithms, but candidates have no tool to pre-diagnose how their resume aligns with technical requirements.
3. **Absence of Objective Behavioral Coaching:** Technical talent frequently struggles with behavioral and managerial rounds (STAR methodology: Situation, Task, Action, Result) or expressing design trade-offs clearly under timed conditions.
4. **Hallucination in Generic AI Tools:** Off-the-shelf consumer chatbots frequently generate inaccurate syntax, fabricate library methods, and lack grounded enterprise context, leading candidates to memorize incorrect answers.

---

### 2. Significance & Impact

Bridging the interview preparation gap has immense economic and educational significance:
- **Employability Transformation:** Empowers students from non-tier-1 institutions and underrepresented backgrounds to receive elite, enterprise-grade mock interview training.
- **Measurable Skill Readiness:** Provides quantifiable readiness scores (0-100) and pinpointed skill gap identification rather than vague encouragement.
- **Enterprise Alignment:** Directly trains candidates on modern enterprise paradigms—stateless microservices, hybrid cloud, data consistency, and ethical AI—reducing onboarding overhead for hiring companies like IBM.

---

### 3. Target Users & Pain Points

#### User Group A: Students & Fresh Graduates
- **Pain Points:**
  - Overwhelmed by disparate syllabus topics (DSA, DBMS, OS, Networks, OOP).
  - Lack experience structuring behavioral and HR answers.
  - Nervousness and poor verbal communication during live interviews.
- **Solution Benefit:**
  - Structured foundational question generator, speech-to-text practice with timers, and instant constructive feedback.

#### User Group B: Experienced Professionals (2–5+ Years)
- **Pain Points:**
  - Need to articulate complex architectural trade-offs (microservices, Saga pattern, ACID vs BASE, latency SLAs).
  - Difficulty pivoting from individual contributor roles to leadership/scenario-based interview expectations.
- **Solution Benefit:**
  - Scenario-based architecture questions, distributed systems challenges, and deep model answers with trade-off analysis.

#### User Group C: Active Job Seekers & Career Changers
- **Pain Points:**
  - Unclear why their resumes fail automated screenings.
  - Require targeted daily roadmaps to close skill gaps in limited preparation time.
- **Solution Benefit:**
  - IBM Docling resume parsing identifies missing prerequisite skills and synthesizes an actionable 7-day learning roadmap.

---

### 4. Solution Overview: The IBM Granite Interview Trainer Agent

The **IBM Granite Interview Trainer Agent** is an end-to-end, full-stack, enterprise-grade AI coaching application powered exclusively by **IBM Cloud** technologies:
- **IBM Granite 3.0 (`ibm/granite-3-8b-instruct`):** Acts as the primary foundation model reasoning engine for question generation, answer evaluation, professional rewriting, and roadmap planning.
- **IBM Docling Core:** Converts resumes (PDF, DOCX, TXT) into hierarchical structural trees to extract skills, detect gaps, and benchmark profile readiness.
- **IBM Langflow & IBM Slate Embeddings (`ibm/slate-30m-english-rtr`):** Implements an enterprise RAG pipeline retrieving verified technical, behavioral, and company-specific documents to eliminate hallucinations.
- **IBM Cloud Object Storage (COS) & Cloudant:** Protects candidate documents and provides persistent session history.
- **Web Speech Voice Interaction:** Enables candidates to speak answers aloud in simulated real-time interview conditions.
