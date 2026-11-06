"""
Pydantic Schemas for the IBM Granite Interview Trainer Agent
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field

class CandidateRegister(BaseModel):
    name: str = Field(..., example="Aarav Sharma")
    email: str = Field(..., example="aarav.sharma@example.com")
    password: Optional[str] = "ibm_skillsbuild_2026"

class CandidateProfile(BaseModel):
    name: str = Field(..., example="Aarav Sharma")
    email: str = Field(..., example="aarav.sharma@example.com")
    experience_level: str = Field(..., example="Fresher")  # Fresher, 0-2 years, 2-5 years, 5+ years
    education: str = Field(..., example="B.Tech in Computer Science")
    college: str = Field(..., example="National Institute of Technology")
    target_role: str = Field(..., example="Cloud Application Developer")
    industry: str = Field(..., example="Information Technology & Cloud Services")
    technical_skills: List[str] = Field(default_factory=list, example=["Python", "Cloud Computing", "REST APIs", "SQL"])
    programming_languages: List[str] = Field(default_factory=list, example=["Python", "Java", "SQL"])
    preferred_company: Optional[str] = Field(default="IBM", example="IBM")
    interview_type: str = Field(default="Mixed", example="Mixed")  # Technical, HR, Managerial, Behavioral, Mixed
    difficulty: str = Field(default="Intermediate", example="Intermediate")  # Beginner, Intermediate, Advanced
    additional_requirements: Optional[str] = Field(default="", example="Focus on cloud microservices and behavioral STAR responses")
    resume_filename: Optional[str] = None
    resume_text: Optional[str] = None

class ResumeAnalysis(BaseModel):
    candidate_name: str
    target_role: str
    extracted_skills: List[str]
    missing_skills: List[str]
    detected_keywords: List[str]
    education_summary: str
    experience_summary: str
    projects_summary: List[str]
    profile_readiness_score: int  # 0 to 100
    docling_pages_parsed: int
    docling_elements_count: int
    recommendations: List[str]

class QuestionItem(BaseModel):
    id: str
    category: str  # Technical, HR, Behavioral, Scenario-Based
    difficulty: str  # Beginner, Intermediate, Advanced
    question: str
    expected_criteria: List[str]
    model_answer: str
    explanation: str
    follow_up_questions: List[str]
    interview_tips: str

class QuestionGenerationRequest(BaseModel):
    candidate_profile: Optional[CandidateProfile] = None
    candidate_email: Optional[str] = None
    job_role: Optional[str] = "Cloud Application Developer"
    interview_type: Optional[str] = "Mixed"
    difficulty: Optional[str] = "Intermediate"
    num_questions: Optional[int] = 5
    custom_topic: Optional[str] = None

class QuestionGenerationResponse(BaseModel):
    generated_by: str = "IBM Granite (watsonx.ai)"
    model_name: str = "ibm/granite-3-8b-instruct"
    target_role: str
    interview_type: str
    difficulty: str
    rag_sources_used: List[str] = []
    questions: List[QuestionItem]

class AnswerEvaluationRequest(BaseModel):
    question: str
    category: str = "Technical"
    user_answer: str
    target_role: str = "Cloud Application Developer"
    difficulty: str = "Intermediate"
    candidate_email: Optional[str] = None

class MetricScore(BaseModel):
    score: int  # 1 to 10
    feedback: str

class AnswerEvaluationResponse(BaseModel):
    overall_score: int  # 0 to 100
    technical_correctness: MetricScore
    relevance: MetricScore
    clarity: MetricScore
    communication: MetricScore
    completeness: MetricScore
    problem_solving_approach: MetricScore
    strengths: List[str]
    improvement_areas: List[str]
    better_sample_answer: str
    why_better_explanation: str
    beginner_version: str
    additional_points_to_include: List[str]
    ethical_disclaimer: str = (
        "IBM SkillsBuild Responsible AI Notice: AI-generated evaluations and scores are "
        "designed purely for preparation coaching and self-assessment, not as guaranteed "
        "predictions of real hiring decisions or company employment outcomes."
    )

class MockInterviewStartRequest(BaseModel):
    interview_type: str = "Mixed"
    difficulty: str = "Intermediate"
    num_questions: int = 5
    job_role: Optional[str] = "Cloud Application Developer"
    candidate_email: Optional[str] = None

class MockInterviewAnswerSubmit(BaseModel):
    session_id: str
    question_id: str
    user_answer: str
    time_taken_seconds: Optional[int] = 60

class DailyTask(BaseModel):
    day: int
    focus_topic: str
    technical_prep: str
    hr_behavioral_prep: str
    practice_questions: List[str]
    revision_activity: str

class PreparationRoadmap(BaseModel):
    candidate_name: str
    target_role: str
    experience_level: str
    generated_at: str
    daily_tasks: List[DailyTask]
    key_improvement_priorities: List[str]
    recommended_mock_milestones: List[str]
    ibm_skillsbuild_recommended_modules: List[str]

class SettingsUpdate(BaseModel):
    WATSONX_APIKEY: Optional[str] = None
    WATSONX_PROJECT_ID: Optional[str] = None
    WATSONX_URL: Optional[str] = None
    WATSONX_MODEL_ID: Optional[str] = None
    WATSONX_EMBEDDING_MODEL_ID: Optional[str] = None
    IBM_COS_APIKEY: Optional[str] = None
    IBM_COS_SERVICE_INSTANCE_ID: Optional[str] = None
    IBM_COS_ENDPOINT: Optional[str] = None
    IBM_COS_BUCKET_NAME: Optional[str] = None
    IBM_CLOUDANT_URL: Optional[str] = None
    IBM_CLOUDANT_APIKEY: Optional[str] = None
