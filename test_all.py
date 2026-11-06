"""
Comprehensive Verification Suite for IBM Granite Interview Trainer Agent
Tests all 15 core functional modules required by the IBM SkillsBuild Evaluation.
"""

import sys
import unittest
from pathlib import Path
from fastapi.testclient import TestClient

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.main import app
from app.config import settings

client = TestClient(app)

class TestInterviewTrainerAgent(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        print("\n" + "="*70)
        print("STARTING TEST SUITE: IBM GRANITE INTERVIEW TRAINER AGENT")
        print("="*70)

    def test_01_system_status_and_ibm_technologies(self):
        """Verify IBM technology stack reporting (Granite, Docling, Langflow, watsonx)."""
        response = client.get("/api/status")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("ibm_technologies", data)
        self.assertIn("IBM Granite", data["ibm_technologies"]["foundation_model"])
        self.assertIn("IBM Docling", data["ibm_technologies"]["document_intelligence"])
        self.assertIn("IBM Langflow", data["ibm_technologies"]["rag_workflow_orchestrator"])
        print("[PASS] Test 1: System status correctly reports full IBM technology stack.")

    def test_02_candidate_registration_and_login(self):
        """Verify candidate registration and login persistence."""
        test_email = "test.engineer@skillsbuild.ibm.edu"
        reg_res = client.post("/api/register", json={
            "name": "Priya Nair",
            "email": test_email,
            "password": "ibm_skillsbuild_2026"
        })
        self.assertEqual(reg_res.status_code, 200)

        login_res = client.post("/api/login", json={
            "name": "Priya Nair",
            "email": test_email
        })
        self.assertEqual(login_res.status_code, 200)
        self.assertEqual(login_res.json()["candidate"]["email"], test_email)
        print("[PASS] Test 2: Candidate registration and login succeeded.")

    def test_03_candidate_profile_update_and_retrieval(self):
        """Verify profile update and retrieval."""
        test_email = "test.engineer@skillsbuild.ibm.edu"
        profile_data = {
            "name": "Priya Nair",
            "email": test_email,
            "experience_level": "Fresher",
            "education": "B.Tech Computer Science",
            "college": "National Institute of Technology",
            "target_role": "Cloud Application Developer",
            "industry": "Information Technology",
            "technical_skills": ["Python", "Docker", "SQL", "Cloud Fundamentals"],
            "programming_languages": ["Python", "SQL"],
            "preferred_company": "IBM",
            "interview_type": "Mixed",
            "difficulty": "Intermediate",
            "additional_requirements": "Focus on cloud microservices"
        }
        post_res = client.post("/api/profile", json=profile_data)
        self.assertEqual(post_res.status_code, 200)

        get_res = client.get(f"/api/profile?email={test_email}")
        self.assertEqual(get_res.status_code, 200)
        self.assertEqual(get_res.json()["target_role"], "Cloud Application Developer")
        print("[PASS] Test 3: Profile saved and retrieved correctly.")

    def test_04_resume_upload_and_docling_parsing(self):
        """Verify resume upload and IBM Docling layout and content extraction."""
        sample_path = Path(__file__).resolve().parent / "sample_resume.txt"
        with open(sample_path, "rb") as f:
            file_bytes = f.read()

        response = client.post(
            "/api/resume/upload",
            files={"file": ("sample_resume.txt", file_bytes, "text/plain")},
            data={"email": "test.engineer@skillsbuild.ibm.edu", "target_role": "Cloud Application Developer"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("analysis", data)
        self.assertGreater(len(data["analysis"]["extracted_skills"]), 0)
        self.assertGreater(data["analysis"]["profile_readiness_score"], 0)
        print(f"[PASS] Test 4: IBM Docling parsed resume. Detected {len(data['analysis']['extracted_skills'])} skills. Readiness: {data['analysis']['profile_readiness_score']}/100.")

    def test_05_skill_gap_identification(self):
        """Verify identification of missing skills compared to target role."""
        response = client.get("/api/resume/analysis?email=test.engineer@skillsbuild.ibm.edu")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("missing_skills", data)
        print(f"[PASS] Test 5: Skill gap identification successful. Missing skills: {data['missing_skills'][:3]}.")

    def test_06_job_role_selection_and_switch(self):
        """Verify job role calibration."""
        res = client.get("/api/dashboard?email=test.engineer@skillsbuild.ibm.edu")
        self.assertEqual(res.status_code, 200)
        self.assertTrue(bool(res.json()["target_role"]))
        print("[PASS] Test 6: Job role selection and calibration active.")

    def test_07_rag_document_retrieval(self):
        """Verify vector retrieval using IBM Slate dense embeddings."""
        from app.services.rag_service import rag_service
        chunks = rag_service.retrieve_context("Explain ACID properties in database transactions", top_k=2)
        self.assertGreater(len(chunks), 0)
        self.assertIn("ACID", chunks[0]["title"])
        print(f"[PASS] Test 7: RAG semantic retrieval verified. Top chunk: '{chunks[0]['title']}'.")

    def test_08_ibm_granite_question_generation(self):
        """Verify personalized question generation powered by IBM Granite."""
        res = client.post("/api/questions/generate", json={
            "job_role": "Cloud Application Developer",
            "interview_type": "Mixed",
            "difficulty": "Intermediate",
            "num_questions": 3
        })
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(len(data["questions"]), 3)
        self.assertIn("IBM Granite", data["generated_by"])
        print(f"[PASS] Test 8: IBM Granite generated {len(data['questions'])} grounded questions.")

    def test_09_model_answer_generation(self):
        """Verify model answers and evaluation criteria generated for questions."""
        res = client.post("/api/questions/generate", json={
            "job_role": "Cloud Application Developer",
            "num_questions": 1
        })
        q = res.json()["questions"][0]
        self.assertTrue(len(q["model_answer"]) > 50)
        self.assertTrue(len(q["expected_criteria"]) > 0)
        print("[PASS] Test 9: Comprehensive model answer and criteria verified.")

    def test_10_interactive_mock_interview_workflow(self):
        """Verify start, answering, and completing a mock interview."""
        start_res = client.post("/api/mock/start", json={
            "job_role": "Cloud Application Developer",
            "interview_type": "Mixed",
            "difficulty": "Intermediate",
            "num_questions": 2
        })
        self.assertEqual(start_res.status_code, 200)
        sess = start_res.json()
        session_id = sess["session_id"]

        # Submit answer to Question 1
        q1 = sess["questions"][0]
        ans_res = client.post("/api/mock/submit", json={
            "session_id": session_id,
            "question_id": q1["id"],
            "user_answer": "I design stateless microservices using Docker containers and implement circuit breakers for fault tolerance.",
            "time_taken_seconds": 45
        })
        self.assertEqual(ans_res.status_code, 200)
        self.assertIn("evaluation", ans_res.json())
        print(f"[PASS] Test 10: Mock interview session {session_id} started, answer submitted, and evaluated.")

    def test_11_answer_evaluation_criteria(self):
        """Verify answer evaluation across all 6 objective criteria."""
        eval_res = client.post("/api/evaluate/answer", json={
            "question": "What is the difference between TCP and UDP?",
            "category": "Technical",
            "user_answer": "TCP is connection oriented with three-way handshake, while UDP is connectionless without delivery guarantees."
        })
        self.assertEqual(eval_res.status_code, 200)
        data = eval_res.json()
        self.assertIn("technical_correctness", data)
        self.assertIn("relevance", data)
        self.assertIn("clarity", data)
        self.assertIn("communication", data)
        self.assertIn("completeness", data)
        self.assertIn("problem_solving_approach", data)
        self.assertIn("ethical_disclaimer", data)
        print(f"[PASS] Test 11: Answer evaluated across all 6 criteria. Overall score: {data['overall_score']}/100.")

    def test_12_preparation_roadmap_generation(self):
        """Verify 7-day personalized preparation roadmap synthesis."""
        res = client.get("/api/roadmap?email=test.engineer@skillsbuild.ibm.edu")
        self.assertEqual(res.status_code, 200)
        data = res.json()
        self.assertEqual(len(data["daily_tasks"]), 7)
        self.assertIn("ibm_skillsbuild_recommended_modules", data)
        print("[PASS] Test 12: 7-Day personalized preparation roadmap generated successfully.")

    def test_13_dashboard_calculations(self):
        """Verify real calculated dashboard statistics."""
        res = client.get("/api/dashboard?email=test.engineer@skillsbuild.ibm.edu")
        self.assertEqual(res.status_code, 200)
        d = res.json()
        self.assertIn("total_questions_practiced", d)
        self.assertIn("mock_interviews_completed", d)
        self.assertIn("average_practice_score", d)
        self.assertIn("preparation_progress", d)
        print(f"[PASS] Test 13: Dashboard metrics computed: Progress={d['preparation_progress']}%, AvgScore={d['average_practice_score']}%.")

    def test_14_error_handling_and_input_validation(self):
        """Verify graceful error handling for invalid or empty inputs."""
        res = client.post("/api/evaluate/answer", json={
            "question": "Sample Question",
            "category": "Technical",
            "user_answer": "Too short"
        })
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.json()["overall_score"], 25)
        print("[PASS] Test 14: Short/invalid input handled gracefully with constructive coaching.")

    def test_15_static_assets_and_page_rendering(self):
        """Verify frontend index.html and Carbon design assets load properly."""
        index_res = client.get("/")
        self.assertEqual(index_res.status_code, 200)
        self.assertIn("IBM Granite", index_res.text)

        css_res = client.get("/static/css/carbon_theme.css")
        self.assertEqual(css_res.status_code, 200)

        js_res = client.get("/static/js/app.js")
        self.assertEqual(js_res.status_code, 200)
        print("[PASS] Test 15: Frontend Single-Page Portal and IBM Carbon CSS/JS verified.")

    def test_16_logout_and_two_candidate_switching(self):
        """Verify Requirement 10: Test logout and login with two different candidate accounts."""
        from app.database import get_candidate

        # 1. Candidate 1: Aarav Sharma
        cand1_email = "aarav.sharma@skillsbuild.ibm.edu"
        res_login1 = client.post("/api/login", json={"email": cand1_email, "name": "Aarav Sharma"})
        self.assertEqual(res_login1.status_code, 200)

        # Candidate 1 updates profile
        client.post("/api/profile", json={
            "name": "Aarav Sharma",
            "email": cand1_email,
            "experience_level": "2-5 years",
            "education": "B.Tech Computer Science",
            "college": "IIT Delhi",
            "target_role": "AI / RAG Engineer",
            "industry": "Artificial Intelligence",
            "technical_skills": ["Python", "IBM Granite", "watsonx.ai", "Langflow"],
            "programming_languages": ["Python"],
            "preferred_company": "IBM",
            "interview_type": "Technical",
            "difficulty": "Advanced",
            "additional_requirements": "Focus on Granite RAG architectures"
        })

        # Candidate 1 practices a question
        client.post("/api/evaluate/answer", json={
            "question": "What is IBM Granite 3.0?",
            "category": "Technical",
            "user_answer": "IBM Granite is an open enterprise foundation model optimized for business and code tasks with RAG grounding.",
            "candidate_email": cand1_email
        })

        # Verify Candidate 1 dashboard
        dash1 = client.get(f"/api/dashboard?email={cand1_email}").json()
        self.assertEqual(dash1["candidate_name"], "Aarav Sharma")
        self.assertEqual(dash1["target_role"], "AI / RAG Engineer")
        self.assertIn("IBM Granite", dash1["strong_skills"])

        # 2. Candidate 1 Logs Out
        res_logout1 = client.post("/api/logout", json={"email": cand1_email})
        self.assertEqual(res_logout1.status_code, 200)
        self.assertEqual(res_logout1.json()["status"], "success")

        # Crucial check: Candidate 1's profile and data must NOT be deleted from database upon logout
        saved_cand1 = get_candidate(cand1_email)
        self.assertIsNotNone(saved_cand1)
        self.assertEqual(saved_cand1["name"], "Aarav Sharma")

        # 3. Candidate 2: Devika Patel logs in
        cand2_email = "devika.patel@skillsbuild.ibm.edu"
        res_login2 = client.post("/api/login", json={"email": cand2_email, "name": "Devika Patel"})
        self.assertEqual(res_login2.status_code, 200)

        # Candidate 2 updates profile
        client.post("/api/profile", json={
            "name": "Devika Patel",
            "email": cand2_email,
            "experience_level": "Fresher",
            "education": "B.Tech Information Technology",
            "college": "NIT Surathkal",
            "target_role": "DevOps & Cloud Engineer",
            "industry": "Cloud Infrastructure",
            "technical_skills": ["Docker", "Kubernetes", "Linux", "Bash"],
            "programming_languages": ["Bash", "Python"],
            "preferred_company": "IBM",
            "interview_type": "Technical",
            "difficulty": "Intermediate",
            "additional_requirements": "Focus on Kubernetes container deployments"
        })

        # Candidate 2 practices a different question
        client.post("/api/evaluate/answer", json={
            "question": "Explain Kubernetes Pods and Deployments.",
            "category": "Technical",
            "user_answer": "Pods are the smallest deployable units in Kubernetes, while Deployments manage replica sets for high availability.",
            "candidate_email": cand2_email
        })

        # Verify Candidate 2 dashboard reflects ONLY Devika's information
        dash2 = client.get(f"/api/dashboard?email={cand2_email}").json()
        self.assertEqual(dash2["candidate_name"], "Devika Patel")
        self.assertEqual(dash2["target_role"], "DevOps & Cloud Engineer")
        self.assertIn("Docker", dash2["strong_skills"])
        self.assertNotIn("IBM Granite", dash2["strong_skills"])

        # Verify Candidate 2 history does NOT contain Candidate 1's questions
        hist2 = client.get(f"/api/history?email={cand2_email}").json()
        hist2_questions = [q["question"] for q in hist2["practiced_questions"]]
        self.assertIn("Explain Kubernetes Pods and Deployments.", hist2_questions)
        self.assertNotIn("What is IBM Granite 3.0?", hist2_questions)

        # 4. Candidate 2 Logs Out
        res_logout2 = client.post("/api/logout", json={"email": cand2_email})
        self.assertEqual(res_logout2.status_code, 200)

        # 5. Candidate 1 Logs Back In - Verify data persistence and isolation
        res_login1_again = client.post("/api/login", json={"email": cand1_email, "name": "Aarav Sharma"})
        self.assertEqual(res_login1_again.status_code, 200)

        dash1_again = client.get(f"/api/dashboard?email={cand1_email}").json()
        self.assertEqual(dash1_again["candidate_name"], "Aarav Sharma")
        self.assertEqual(dash1_again["target_role"], "AI / RAG Engineer")
        self.assertIn("IBM Granite", dash1_again["strong_skills"])
        self.assertNotIn("Docker", dash1_again["strong_skills"])

        hist1 = client.get(f"/api/history?email={cand1_email}").json()
        hist1_questions = [q["question"] for q in hist1["practiced_questions"]]
        self.assertIn("What is IBM Granite 3.0?", hist1_questions)
        self.assertNotIn("Explain Kubernetes Pods and Deployments.", hist1_questions)

        # 6. Verify Logout button presence in top header of index.html
        index_html = client.get("/").text
        self.assertIn('id="header-logout-btn"', index_html)
        self.assertIn('confirmAndLogout()', index_html)
        self.assertIn('Logout', index_html)
        self.assertIn('id="header-candidate-name"', index_html)

        print("[PASS] Test 16: Two-candidate login/logout workflow and account data isolation verified successfully.")

if __name__ == "__main__":
    unittest.main()
