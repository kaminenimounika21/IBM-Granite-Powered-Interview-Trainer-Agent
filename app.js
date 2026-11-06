/**
 * IBM Granite Interview Trainer Agent - Client Controller
 * Manages 15 views, state reactivity, speech recognition, and API bindings.
 */

// Global Application State
const state = {
  currentView: 'welcome-view',
  candidate: null,
  mockSession: {
    sessionId: null,
    questions: [],
    currentIndex: 0,
    timerInterval: null,
    secondsElapsed: 0
  },
  generatedQuestions: [],
  speechRecognition: null,
  isRecording: false
};

// Initialize on DOM load
document.addEventListener('DOMContentLoaded', () => {
  initCandidateSession();
  initNavigation();
  initSpeechRecognition();
  loadSystemStatus();
  updateHeaderUserDisplay();
  if (state.candidate) {
    loadDashboardData();
  }
  setupEventListeners();
});

// ----------------- Candidate Authentication & Session Management ----------------- //

function initCandidateSession() {
  const isLoggedOut = sessionStorage.getItem('ibm_is_logged_out');
  if (isLoggedOut === 'true') {
    state.candidate = null;
    return;
  }
  const stored = localStorage.getItem('ibm_candidate_session');
  if (stored) {
    try {
      state.candidate = JSON.parse(stored);
      return;
    } catch (e) {
      console.warn('Failed to parse candidate session:', e);
    }
  }
  // Default active candidate session on initial arrival
  state.candidate = {
    email: 'alex.chen@skillsbuild.ibm.edu',
    name: 'Alex Chen',
    target_role: 'Cloud Application Developer',
    experience_level: 'Fresher'
  };
}

function updateHeaderUserDisplay() {
  const nameEl = document.getElementById('header-candidate-name');
  const logoutBtn = document.getElementById('header-logout-btn');
  const userBadge = document.getElementById('header-user-badge');

  if (state.candidate && state.candidate.name) {
    if (nameEl) nameEl.textContent = state.candidate.name;
    if (logoutBtn) logoutBtn.style.display = 'inline-flex';
    if (userBadge) {
      userBadge.style.display = 'flex';
      userBadge.title = `Authenticated as ${state.candidate.name} (${state.candidate.email})`;
    }
  } else {
    if (nameEl) nameEl.textContent = 'Not Signed In';
    if (logoutBtn) logoutBtn.style.display = 'none';
    if (userBadge) {
      userBadge.style.display = 'flex';
      userBadge.title = 'Please sign in or register';
    }
  }
}

function setCandidateSession(cand) {
  state.candidate = cand;
  sessionStorage.removeItem('ibm_is_logged_out');
  localStorage.setItem('ibm_candidate_session', JSON.stringify(cand));
  updateHeaderUserDisplay();
}

async function confirmAndLogout() {
  const confirmed = window.confirm("Are you sure you want to log out?");
  if (!confirmed) return;

  const currentEmail = state.candidate ? state.candidate.email : null;
  const currentName = state.candidate ? state.candidate.name : 'Candidate';

  try {
    await fetch('/api/logout', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email: currentEmail })
    });
  } catch (e) {
    console.warn('Logout notification error:', e);
  }

  // Clear authentication session securely
  localStorage.removeItem('ibm_candidate_session');
  sessionStorage.setItem('ibm_is_logged_out', 'true');

  state.candidate = null;
  state.mockSession = {
    sessionId: null,
    questions: [],
    currentIndex: 0,
    timerInterval: null,
    secondsElapsed: 0
  };
  state.generatedQuestions = [];

  // Update header display
  updateHeaderUserDisplay();

  // Reset auth input fields so next candidate can log in freshly
  const authName = document.getElementById('auth-name');
  const authEmail = document.getElementById('auth-email');
  const authPassword = document.getElementById('auth-password');
  const authMsg = document.getElementById('auth-status-msg');

  if (authName) authName.value = '';
  if (authEmail) authEmail.value = '';
  if (authPassword) authPassword.value = '';
  if (authMsg) {
    authMsg.innerHTML = `
      <div style="background: #edf5ff; border: 1px solid #0f62fe; padding: 0.85rem 1rem; color: #0043ce; margin-top: 1rem; border-radius: 2px;">
        <strong>✓ Logged Out:</strong> Candidate ${currentName} has logged out securely. The next candidate can sign in or register below.
      </div>
    `;
  }

  navigateTo('auth-view');
}

// Expose globally for onclick events
window.confirmAndLogout = confirmAndLogout;
window.setCandidateSession = setCandidateSession;

// ----------------- Navigation Router (15 Views) ----------------- //

function navigateTo(viewId) {
  const authenticatedViews = [
    'dashboard-view', 'profile-view', 'resume-upload-view',
    'resume-analysis-view', 'mock-interview-view', 'answer-eval-view',
    'roadmap-view', 'history-view'
  ];

  if (!state.candidate && authenticatedViews.includes(viewId)) {
    alert('Please sign in or register to access candidate interview features.');
    viewId = 'auth-view';
  }

  state.currentView = viewId;

  // Update views
  document.querySelectorAll('.page-view').forEach(view => {
    view.classList.remove('active');
  });
  const targetView = document.getElementById(viewId);
  if (targetView) {
    targetView.classList.add('active');
  }

  // Update sidebar active links
  document.querySelectorAll('.ibm-nav-item').forEach(item => {
    item.classList.remove('active');
    if (item.getAttribute('data-target') === viewId) {
      item.classList.add('active');
    }
  });

  window.scrollTo({ top: 0, behavior: 'smooth' });

  // Lifecycle view loaders
  if (state.candidate) {
    if (viewId === 'dashboard-view') loadDashboardData();
    if (viewId === 'profile-view') loadProfileData();
    if (viewId === 'resume-analysis-view') loadResumeAnalysis();
    if (viewId === 'roadmap-view') loadRoadmapData();
    if (viewId === 'history-view') loadPracticeHistory();
  }
  if (viewId === 'kb-management-view') loadKnowledgeBase();
  if (viewId === 'settings-view') loadSettings();
}

function initNavigation() {
  document.querySelectorAll('.ibm-nav-item').forEach(item => {
    item.addEventListener('click', (e) => {
      e.preventDefault();
      const target = item.getAttribute('data-target');
      if (target) navigateTo(target);
    });
  });
}

// ----------------- Speech-to-Text / Audio Input ----------------- //

function initSpeechRecognition() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (SpeechRecognition) {
    state.speechRecognition = new SpeechRecognition();
    state.speechRecognition.continuous = true;
    state.speechRecognition.interimResults = true;
    state.speechRecognition.lang = 'en-US';

    state.speechRecognition.onresult = (event) => {
      let transcript = '';
      for (let i = event.resultIndex; i < event.results.length; i++) {
        transcript += event.results[i][0].transcript;
      }
      const activeTextarea = document.querySelector('.active-voice-target');
      if (activeTextarea) {
        activeTextarea.value = transcript;
      }
    };

    state.speechRecognition.onerror = (e) => {
      console.warn('Speech recognition warning:', e.error);
      stopVoiceRecording();
    };

    state.speechRecognition.onend = () => {
      state.isRecording = false;
      updateVoiceButtons();
    };
  }
}

function toggleVoiceRecording(targetTextareaId, btnElement) {
  if (!state.speechRecognition) {
    alert('Voice recognition is not supported in this browser. Please type your response directly into the text box.');
    return;
  }

  const textarea = document.getElementById(targetTextareaId);
  if (!state.isRecording) {
    document.querySelectorAll('.form-textarea').forEach(t => t.classList.remove('active-voice-target'));
    textarea.classList.add('active-voice-target');
    try {
      state.speechRecognition.start();
      state.isRecording = true;
      btnElement.classList.add('recording');
      btnElement.innerHTML = `<span>⏹ Stop Voice Recording</span>`;
    } catch (e) {
      console.error(e);
    }
  } else {
    stopVoiceRecording();
  }
}

function stopVoiceRecording() {
  if (state.speechRecognition && state.isRecording) {
    state.speechRecognition.stop();
  }
  state.isRecording = false;
  updateVoiceButtons();
}

function updateVoiceButtons() {
  document.querySelectorAll('.voice-recorder-btn').forEach(btn => {
    btn.classList.remove('recording');
    btn.innerHTML = `<span>🎙 Speak Your Answer (Voice-to-Text)</span>`;
  });
}

// ----------------- System Status & Header ----------------- //

async function loadSystemStatus() {
  try {
    const res = await fetch('/api/status');
    const data = await res.json();
    const statusChip = document.getElementById('system-status-chip');
    if (statusChip && data.watsonx_connection) {
      const mode = data.watsonx_connection.mode;
      const isLive = data.watsonx_connection.configured;
      statusChip.innerHTML = `
        <span class="ibm-chip-dot ${isLive ? '' : 'warning'}"></span>
        <span>IBM Granite 3.0: ${isLive ? 'Live watsonx.ai' : 'Granite Prompt Mode (Ready)'}</span>
      `;
    }
  } catch (e) {
    console.error('Status fetch error:', e);
  }
}

// ----------------- Dashboard View Loader ----------------- //

async function loadDashboardData() {
  try {
    const res = await fetch(`/api/dashboard?email=${encodeURIComponent(state.candidate.email)}`);
    const d = await res.json();

    document.getElementById('dash-candidate-name').textContent = d.candidate_name;
    document.getElementById('dash-target-role').textContent = d.target_role;
    document.getElementById('dash-progress-text').textContent = `${d.preparation_progress}% Complete`;
    document.getElementById('dash-progress-fill').style.width = `${d.preparation_progress}%`;

    document.getElementById('metric-total-q').textContent = d.total_questions_practiced;
    document.getElementById('metric-mocks-count').textContent = d.mock_interviews_completed;
    document.getElementById('metric-avg-score').textContent = `${d.average_practice_score}%`;
    document.getElementById('metric-readiness').textContent = `${d.resume_readiness_score}/100`;

    // Strong skills
    const strongSkillsContainer = document.getElementById('dash-strong-skills');
    strongSkillsContainer.innerHTML = d.strong_skills.map(s => `<span class="ibm-tag tag-blue">${s}</span>`).join('');

    // Missing skills
    const gapSkillsContainer = document.getElementById('dash-skill-gaps');
    gapSkillsContainer.innerHTML = d.improvement_areas.map(s => `<span class="ibm-tag tag-purple">${s}</span>`).join('');

    // Recommended activities
    const actContainer = document.getElementById('dash-recommended-activities');
    actContainer.innerHTML = d.recommended_activities.map(act => `
      <div style="background: #ffffff; border: 1px solid #e0e0e0; padding: 0.85rem 1rem; margin-bottom: 0.5rem; display: flex; justify-content: space-between; align-items: center;">
        <div>
          <span class="ibm-tag tag-gray" style="font-size: 11px;">${act.type}</span>
          <strong style="font-size: 13px; color: #161616;">${act.title}</strong>
        </div>
        <span class="ibm-tag tag-blue" style="font-size: 11px;">${act.badge}</span>
      </div>
    `).join('');
  } catch (e) {
    console.error('Dashboard load error:', e);
  }
}

// ----------------- Profile View Loader & Saver ----------------- //

async function loadProfileData() {
  try {
    const res = await fetch(`/api/profile?email=${encodeURIComponent(state.candidate.email)}`);
    const p = await res.json();
    if (!p) return;

    document.getElementById('prof-name').value = p.name || '';
    document.getElementById('prof-email').value = p.email || '';
    document.getElementById('prof-experience').value = p.experience_level || 'Fresher';
    document.getElementById('prof-education').value = p.education || '';
    document.getElementById('prof-college').value = p.college || '';
    document.getElementById('prof-target-role').value = p.target_role || 'Cloud Application Developer';
    document.getElementById('prof-industry').value = p.industry || 'Information Technology & Cloud Services';
    document.getElementById('prof-tech-skills').value = (p.technical_skills || []).join(', ');
    document.getElementById('prof-prog-langs').value = (p.programming_languages || []).join(', ');
    document.getElementById('prof-preferred-company').value = p.preferred_company || 'IBM';
    document.getElementById('prof-interview-type').value = p.interview_type || 'Mixed';
    document.getElementById('prof-difficulty').value = p.difficulty || 'Intermediate';
    document.getElementById('prof-additional-reqs').value = p.additional_requirements || '';
  } catch (e) {
    console.error('Profile load error:', e);
  }
}

async function saveProfileData() {
  const payload = {
    name: document.getElementById('prof-name').value,
    email: document.getElementById('prof-email').value,
    experience_level: document.getElementById('prof-experience').value,
    education: document.getElementById('prof-education').value,
    college: document.getElementById('prof-college').value,
    target_role: document.getElementById('prof-target-role').value,
    industry: document.getElementById('prof-industry').value,
    technical_skills: document.getElementById('prof-tech-skills').value.split(',').map(s => s.trim()).filter(Boolean),
    programming_languages: document.getElementById('prof-prog-langs').value.split(',').map(s => s.trim()).filter(Boolean),
    preferred_company: document.getElementById('prof-preferred-company').value,
    interview_type: document.getElementById('prof-interview-type').value,
    difficulty: document.getElementById('prof-difficulty').value,
    additional_requirements: document.getElementById('prof-additional-reqs').value
  };

  try {
    const res = await fetch('/api/profile', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const result = await res.json();
    alert('Candidate profile successfully updated and synchronized with IBM storage!');
    state.candidate.name = payload.name;
    state.candidate.target_role = payload.target_role;
    loadDashboardData();
  } catch (e) {
    alert('Error saving profile: ' + e.message);
  }
}

// ----------------- Resume Upload (IBM Docling) ----------------- //

async function uploadResumeFile() {
  const fileInput = document.getElementById('resume-file-input');
  if (!fileInput.files || fileInput.files.length === 0) {
    alert('Please choose a resume document (PDF, DOCX, or TXT) to upload.');
    return;
  }

  const file = fileInput.files[0];
  const targetRole = document.getElementById('resume-target-role').value;
  const statusDiv = document.getElementById('resume-upload-status');

  statusDiv.style.display = 'block';
  statusDiv.innerHTML = `
    <div style="background: #edf5ff; border: 1px solid #0f62fe; padding: 1rem; color: #0043ce;">
      <strong>Processing with IBM Docling...</strong><br>
      Extracting structural hierarchy, parsing layout trees, and comparing skills against ${targetRole} benchmarks.
    </div>
  `;

  const formData = new FormData();
  formData.append('file', file);
  formData.append('email', state.candidate.email);
  formData.append('target_role', targetRole);

  try {
    const res = await fetch('/api/resume/upload', {
      method: 'POST',
      body: formData
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Upload failed');
    }

    const data = await res.json();
    statusDiv.innerHTML = `
      <div style="background: #defbe6; border: 1px solid #24a148; padding: 1rem; color: #0e6027;">
        <strong>✓ Document Successfully Parsed with IBM Docling!</strong><br>
        Identified ${data.analysis.extracted_skills.length} skills, readiness score of ${data.analysis.profile_readiness_score}/100.
        Vaulted safely in ${data.cos_storage.storage}.
      </div>
    `;

    setTimeout(() => {
      navigateTo('resume-analysis-view');
    }, 1200);
  } catch (e) {
    statusDiv.innerHTML = `
      <div style="background: #ffd7d9; border: 1px solid #da1e28; padding: 1rem; color: #a2191f;">
        <strong>Parsing Alert:</strong> ${e.message}<br>
        You may still enter your skills manually in the <a href="#" onclick="navigateTo('profile-view')">Candidate Profile</a> page.
      </div>
    `;
  }
}

// ----------------- Resume Analysis View ----------------- //

async function loadResumeAnalysis() {
  try {
    const res = await fetch(`/api/resume/analysis?email=${encodeURIComponent(state.candidate.email)}`);
    const a = await res.json();
    if (!a) return;

    document.getElementById('analysis-cand-name').textContent = a.candidate_name;
    document.getElementById('analysis-target-role').textContent = a.target_role;
    document.getElementById('analysis-score-number').textContent = `${a.profile_readiness_score}/100`;
    document.getElementById('analysis-score-bar').style.width = `${a.profile_readiness_score}%`;
    document.getElementById('analysis-docling-meta').textContent = `${a.docling_pages_parsed} Page(s) • ${a.docling_elements_count} Structural Elements Parsed via IBM Docling Core`;

    document.getElementById('analysis-extracted-skills').innerHTML = a.extracted_skills.map(s => `<span class="ibm-tag tag-blue">${s}</span>`).join('');
    document.getElementById('analysis-missing-skills').innerHTML = a.missing_skills.map(s => `<span class="ibm-tag tag-red">${s}</span>`).join('');

    document.getElementById('analysis-education').textContent = a.education_summary;
    document.getElementById('analysis-experience').textContent = a.experience_summary;

    document.getElementById('analysis-projects').innerHTML = a.projects_summary.map(p => `<li>${p}</li>`).join('');
    document.getElementById('analysis-recommendations').innerHTML = a.recommendations.map(r => `<li>${r}</li>`).join('');
    document.getElementById('analysis-docling-markdown').textContent = a.docling_markdown || 'Docling document representation ready.';
  } catch (e) {
    console.error('Analysis load error:', e);
  }
}

// ----------------- AI Question Generator (IBM Granite) ----------------- //

async function generateInterviewQuestions() {
  const role = document.getElementById('gen-job-role').value;
  const type = document.getElementById('gen-type').value;
  const diff = document.getElementById('gen-diff').value;
  const count = parseInt(document.getElementById('gen-count').value, 10);
  const container = document.getElementById('generated-questions-container');

  container.innerHTML = `
    <div style="background: #edf5ff; border: 1px solid #0f62fe; padding: 1.5rem; text-align: center; color: #0043ce;">
      <strong>Invoking IBM Granite 3.0 via watsonx.ai...</strong><br>
      Grounding generation in IBM RAG knowledge base for role '${role}' (${type}, ${diff}).
    </div>
  `;

  try {
    const res = await fetch('/api/questions/generate', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        job_role: role,
        interview_type: type,
        difficulty: diff,
        num_questions: count,
        candidate_email: state.candidate ? state.candidate.email : null
      })
    });
    const data = await res.json();
    state.generatedQuestions = data.questions;

    // Render questions
    container.innerHTML = `
      <div style="margin-bottom: 1rem; color: #525252; font-size: 13px;">
        Generated by: <strong>${data.generated_by}</strong> (${data.model_name})<br>
        RAG Citations: ${data.rag_sources_used.join(' • ')}
      </div>
    ` + data.questions.map((q, idx) => `
      <div class="question-card">
        <div class="question-card-category">
          <span class="ibm-tag tag-blue">${q.category}</span>
          <span class="ibm-tag tag-purple">${q.difficulty}</span>
        </div>
        <div class="question-text">Q${idx + 1}: ${q.question}</div>
        <div style="margin-bottom: 0.75rem;">
          <strong style="font-size: 12px; color: #525252; text-transform: uppercase;">Expected Evaluation Criteria:</strong>
          <ul style="padding-left: 1.25rem; font-size: 13px; color: #161616; margin-top: 0.25rem;">
            ${q.expected_criteria.map(c => `<li>${c}</li>`).join('')}
          </ul>
        </div>
        <div style="display: flex; gap: 0.75rem; margin-top: 1rem;">
          <button class="btn-ibm btn-ibm-ghost" onclick="toggleAnswerBox('ans-${q.id}')">View Model Answer & Tips</button>
          <button class="btn-ibm" onclick="practiceSpecificQuestion(${idx})">Practice This Question</button>
        </div>
        <div id="ans-${q.id}" class="collapsible-box">
          <strong style="color: #0f62fe;">IBM Granite Model Answer:</strong>
          <p style="margin: 0.5rem 0; font-size: 13px; line-height: 1.6;">${q.model_answer}</p>
          <strong style="color: #161616; font-size: 12px;">Explanation:</strong>
          <p style="font-size: 13px; color: #525252; margin-bottom: 0.5rem;">${q.explanation}</p>
          <strong style="color: #161616; font-size: 12px;">Interview Tips:</strong>
          <p style="font-size: 13px; color: #0e6027;">💡 ${q.interview_tips}</p>
        </div>
      </div>
    `).join('');
  } catch (e) {
    container.innerHTML = `<div style="color: #da1e28; padding: 1rem;">Error generating questions: ${e.message}</div>`;
  }
}

function toggleAnswerBox(id) {
  const el = document.getElementById(id);
  if (el) el.classList.toggle('open');
}

function practiceSpecificQuestion(index) {
  const q = state.generatedQuestions[index];
  if (!q) return;
  document.getElementById('eval-question-input').value = q.question;
  document.getElementById('eval-category-select').value = q.category;
  navigateTo('answer-eval-view');
}

// ----------------- Interactive Mock Interview Stepper ----------------- //

async function startMockSession() {
  const type = document.getElementById('mock-type-select').value;
  const count = parseInt(document.getElementById('mock-count-select').value, 10);
  const role = document.getElementById('mock-role-input').value;

  const introPanel = document.getElementById('mock-intro-panel');
  const runnerPanel = document.getElementById('mock-runner-panel');
  const summaryPanel = document.getElementById('mock-summary-panel');

  introPanel.style.display = 'none';
  summaryPanel.style.display = 'none';
  runnerPanel.style.display = 'block';

  try {
    const res = await fetch('/api/mock/start', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        interview_type: type,
        num_questions: count,
        job_role: role,
        candidate_email: state.candidate ? state.candidate.email : null
      })
    });
    const data = await res.json();
    state.mockSession.sessionId = data.session_id;
    state.mockSession.questions = data.questions;
    state.mockSession.currentIndex = 0;
    renderCurrentMockQuestion();
  } catch (e) {
    alert('Error starting mock interview: ' + e.message);
  }
}

function renderCurrentMockQuestion() {
  const q = state.mockSession.questions[state.mockSession.currentIndex];
  const total = state.mockSession.questions.length;
  const idx = state.mockSession.currentIndex + 1;

  document.getElementById('mock-stepper-title').textContent = `Question ${idx} of ${total}`;
  document.getElementById('mock-category-tag').textContent = q.category;
  document.getElementById('mock-difficulty-tag').textContent = q.difficulty;
  document.getElementById('mock-active-question-text').textContent = q.question;

  document.getElementById('mock-user-answer-text').value = '';
  document.getElementById('mock-eval-inline-result').style.display = 'none';

  // Reset and start timer
  clearInterval(state.mockSession.timerInterval);
  state.mockSession.secondsElapsed = 0;
  const timerDisplay = document.getElementById('mock-timer-display');
  timerDisplay.textContent = '00:00';

  state.mockSession.timerInterval = setInterval(() => {
    state.mockSession.secondsElapsed++;
    const mins = String(Math.floor(state.mockSession.secondsElapsed / 60)).padStart(2, '0');
    const secs = String(state.mockSession.secondsElapsed % 60).padStart(2, '0');
    timerDisplay.textContent = `${mins}:${secs}`;
  }, 1000);
}

async function submitMockCurrentAnswer() {
  stopVoiceRecording();
  clearInterval(state.mockSession.timerInterval);

  const userAnswer = document.getElementById('mock-user-answer-text').value.trim();
  if (!userAnswer) {
    alert('Please enter or speak your answer before submitting.');
    return;
  }

  const q = state.mockSession.questions[state.mockSession.currentIndex];
  const submitBtn = document.getElementById('mock-submit-btn');
  submitBtn.disabled = true;
  submitBtn.textContent = 'Evaluating with IBM Granite...';

  try {
    const res = await fetch('/api/mock/submit', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        session_id: state.mockSession.sessionId,
        question_id: q.id,
        user_answer: userAnswer,
        time_taken_seconds: state.mockSession.secondsElapsed
      })
    });
    const data = await res.json();
    const evalData = data.evaluation;

    // Display inline evaluation
    const evalDiv = document.getElementById('mock-eval-inline-result');
    evalDiv.style.display = 'block';
    evalDiv.innerHTML = `
      <div style="background: #ffffff; border: 1px solid #0f62fe; padding: 1.5rem; margin-top: 1rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
          <h3 style="font-size: 18px; color: #0f62fe;">IBM Granite Answer Evaluation</h3>
          <span style="font-size: 24px; font-weight: 700; color: #161616;">Score: ${evalData.overall_score}/100</span>
        </div>
        <div class="dashboard-metrics-grid" style="margin-bottom: 1rem;">
          <div style="background: #f4f4f4; padding: 0.75rem;"><strong>Technical:</strong> ${evalData.technical_correctness.score}/10</div>
          <div style="background: #f4f4f4; padding: 0.75rem;"><strong>Relevance:</strong> ${evalData.relevance.score}/10</div>
          <div style="background: #f4f4f4; padding: 0.75rem;"><strong>Clarity:</strong> ${evalData.clarity.score}/10</div>
          <div style="background: #f4f4f4; padding: 0.75rem;"><strong>Problem Solving:</strong> ${evalData.problem_solving_approach.score}/10</div>
        </div>
        <div style="margin-bottom: 1rem;">
          <strong style="color: #24a148;">Key Strengths:</strong>
          <ul style="padding-left: 1.25rem; font-size: 13px;">${evalData.strengths.map(s => `<li>${s}</li>`).join('')}</ul>
        </div>
        <div style="margin-bottom: 1rem;">
          <strong style="color: #da1e28;">Improvement Areas:</strong>
          <ul style="padding-left: 1.25rem; font-size: 13px;">${evalData.improvement_areas.map(s => `<li>${s}</li>`).join('')}</ul>
        </div>
        <div style="background: #f4f4f4; border-left: 3px solid #0f62fe; padding: 1rem; font-size: 13px; line-height: 1.6;">
          <strong>Enhanced Model Answer by IBM Granite:</strong><br>${evalData.better_sample_answer}
        </div>
        <div style="margin-top: 1.25rem; display: flex; justify-content: flex-end;">
          <button class="btn-ibm" onclick="advanceMockInterview()">${state.mockSession.currentIndex + 1 < state.mockSession.questions.length ? 'Next Question →' : 'Complete Interview & View Summary'}</button>
        </div>
      </div>
    `;
  } catch (e) {
    alert('Error submitting answer: ' + e.message);
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = 'Submit Answer for AI Evaluation';
  }
}

function advanceMockInterview() {
  state.mockSession.currentIndex++;
  if (state.mockSession.currentIndex < state.mockSession.questions.length) {
    renderCurrentMockQuestion();
  } else {
    finishMockInterview();
  }
}

async function finishMockInterview() {
  document.getElementById('mock-runner-panel').style.display = 'none';
  const summaryPanel = document.getElementById('mock-summary-panel');
  summaryPanel.style.display = 'block';

  try {
    const res = await fetch(`/api/mock/session/${state.mockSession.sessionId}`);
    const data = await res.json();
    document.getElementById('mock-summary-score').textContent = `${data.session.average_score}%`;
    document.getElementById('mock-summary-count').textContent = data.session.completed_questions;
    loadDashboardData();
  } catch (e) {
    console.error('Summary error:', e);
  }
}

// ----------------- Standalone Answer Evaluation & Improvement ----------------- //

async function evaluateStandaloneAnswer() {
  stopVoiceRecording();
  const q = document.getElementById('eval-question-input').value;
  const ans = document.getElementById('eval-user-answer-input').value;
  const cat = document.getElementById('eval-category-select').value;
  const container = document.getElementById('standalone-eval-result');

  if (!ans.trim()) {
    alert('Please enter or speak your answer to evaluate.');
    return;
  }

  container.innerHTML = `<div style="padding: 1rem; color: #0f62fe;">Analyzing with IBM Granite...</div>`;

  try {
    const res = await fetch('/api/evaluate/answer', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        question: q,
        category: cat,
        user_answer: ans,
        candidate_email: state.candidate ? state.candidate.email : null
      })
    });
    const data = await res.json();

    container.innerHTML = `
      <div class="ibm-tile" style="margin-top: 1rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1.5rem; border-bottom: 1px solid #e0e0e0; padding-bottom: 0.75rem;">
          <h2 style="font-size: 20px; font-weight: 600;">Overall AI Performance Score</h2>
          <span style="font-size: 32px; font-weight: 700; color: #0f62fe;">${data.overall_score}/100</span>
        </div>
        <div class="dashboard-metrics-grid">
          <div class="metric-card"><div class="metric-label">Technical Correctness</div><div class="metric-value">${data.technical_correctness.score}/10</div><div class="metric-sub">${data.technical_correctness.feedback}</div></div>
          <div class="metric-card"><div class="metric-label">Relevance</div><div class="metric-value">${data.relevance.score}/10</div><div class="metric-sub">${data.relevance.feedback}</div></div>
          <div class="metric-card"><div class="metric-label">Clarity</div><div class="metric-value">${data.clarity.score}/10</div><div class="metric-sub">${data.clarity.feedback}</div></div>
          <div class="metric-card"><div class="metric-label">Communication</div><div class="metric-value">${data.communication.score}/10</div><div class="metric-sub">${data.communication.feedback}</div></div>
          <div class="metric-card"><div class="metric-label">Completeness</div><div class="metric-value">${data.completeness.score}/10</div><div class="metric-sub">${data.completeness.feedback}</div></div>
          <div class="metric-card"><div class="metric-label">Problem Solving</div><div class="metric-value">${data.problem_solving_approach.score}/10</div><div class="metric-sub">${data.problem_solving_approach.feedback}</div></div>
        </div>
        <div style="margin: 1.5rem 0;">
          <strong style="color: #24a148;">Observed Strengths:</strong>
          <ul style="padding-left: 1.25rem; font-size: 13px; margin: 0.4rem 0;">${data.strengths.map(s => `<li>${s}</li>`).join('')}</ul>
        </div>
        <div style="margin: 1.5rem 0;">
          <strong style="color: #da1e28;">Areas for Improvement:</strong>
          <ul style="padding-left: 1.25rem; font-size: 13px; margin: 0.4rem 0;">${data.improvement_areas.map(s => `<li>${s}</li>`).join('')}</ul>
        </div>
        <div class="ibm-tile" style="background: #f4f4f4; border-left: 4px solid #0f62fe;">
          <h3 style="font-size: 15px; color: #0f62fe; margin-bottom: 0.5rem;">Professional Model Answer (IBM Granite):</h3>
          <p style="font-size: 14px; line-height: 1.6; color: #161616;">${data.better_sample_answer}</p>
          <div style="margin-top: 1rem; font-size: 13px; color: #525252;">
            <strong>Why this is better:</strong> ${data.why_better_explanation}
          </div>
          <div style="margin-top: 0.75rem; font-size: 13px; color: #0e6027;">
            <strong>Beginner-Friendly Version:</strong> ${data.beginner_version}
          </div>
        </div>
        <div class="ethical-ai-banner">
          <div>⚖️ <strong>Responsible AI Notice:</strong> ${data.ethical_disclaimer}</div>
        </div>
      </div>
    `;
    loadDashboardData();
  } catch (e) {
    container.innerHTML = `<div style="color: #da1e28;">Error evaluating answer: ${e.message}</div>`;
  }
}

// ----------------- Personalized Preparation Roadmap ----------------- //

async function loadRoadmapData() {
  const container = document.getElementById('roadmap-cards-container');
  container.innerHTML = `<div style="color: #0f62fe; padding: 1rem;">Synthesizing 7-Day Roadmap with IBM Granite...</div>`;

  try {
    const res = await fetch(`/api/roadmap?email=${encodeURIComponent(state.candidate.email)}`);
    const r = await res.json();

    document.getElementById('roadmap-cand-info').textContent = `${r.candidate_name} • Target Role: ${r.target_role} (${r.experience_level})`;

    container.innerHTML = r.daily_tasks.map(task => `
      <div class="ibm-tile" style="border-left: 4px solid #0f62fe;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.75rem;">
          <h3 style="font-size: 16px; font-weight: 600;">Day ${task.day}: ${task.focus_topic}</h3>
          <span class="ibm-tag tag-blue">Task Active</span>
        </div>
        <div style="font-size: 13px; margin-bottom: 0.5rem;">
          <strong>Technical Preparation:</strong> ${task.technical_prep}
        </div>
        <div style="font-size: 13px; margin-bottom: 0.5rem;">
          <strong>HR & Behavioral Coaching:</strong> ${task.hr_behavioral_prep}
        </div>
        <div style="font-size: 13px; margin-bottom: 0.5rem;">
          <strong>Daily Practice Questions:</strong>
          <ul style="padding-left: 1.25rem; margin-top: 0.25rem;">${task.practice_questions.map(q => `<li>${q}</li>`).join('')}</ul>
        </div>
        <div style="font-size: 13px; color: #0e6027;">
          <strong>Daily Revision Activity:</strong> 📝 ${task.revision_activity}
        </div>
      </div>
    `).join('');

    // Recommended SkillsBuild modules
    document.getElementById('roadmap-skillsbuild-courses').innerHTML = r.ibm_skillsbuild_recommended_modules.map(c => `
      <li style="margin-bottom: 0.4rem;">🎓 ${c}</li>
    `).join('');
  } catch (e) {
    container.innerHTML = `<div style="color: #da1e28;">Error loading roadmap: ${e.message}</div>`;
  }
}

// ----------------- Practice History ----------------- //

async function loadPracticeHistory() {
  try {
    const res = await fetch(`/api/history?email=${encodeURIComponent(state.candidate.email)}`);
    const h = await res.json();

    const qBody = document.getElementById('history-questions-table');
    if (h.practiced_questions && h.practiced_questions.length > 0) {
      qBody.innerHTML = h.practiced_questions.map(q => `
        <tr>
          <td style="padding: 0.6rem; border-bottom: 1px solid #e0e0e0;">${q.question.substring(0, 50)}...</td>
          <td style="padding: 0.6rem; border-bottom: 1px solid #e0e0e0;"><span class="ibm-tag tag-blue">${q.category}</span></td>
          <td style="padding: 0.6rem; border-bottom: 1px solid #e0e0e0; font-weight: 600;">${q.score}/100</td>
          <td style="padding: 0.6rem; border-bottom: 1px solid #e0e0e0; font-size: 12px; color: #525252;">${q.created_at}</td>
        </tr>
      `).join('');
    } else {
      qBody.innerHTML = `<tr><td colspan="4" style="padding: 1rem; text-align: center; color: #8d8d8d;">No practice questions answered yet. Start a practice session!</td></tr>`;
    }
  } catch (e) {
    console.error('History load error:', e);
  }
}

// ----------------- Knowledge Base Management ----------------- //

async function loadKnowledgeBase() {
  try {
    const res = await fetch('/api/knowledge-base');
    const kb = await res.json();

    document.getElementById('kb-count-badge').textContent = `${kb.total_documents} Indexed Chunks`;
    document.getElementById('kb-embedding-name').textContent = kb.embedding_model;

    const listContainer = document.getElementById('kb-documents-list');
    listContainer.innerHTML = kb.documents.map(doc => `
      <div style="background: #ffffff; border: 1px solid #e0e0e0; padding: 1rem; margin-bottom: 0.75rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
          <strong style="color: #161616; font-size: 14px;">${doc.title}</strong>
          <span class="ibm-tag tag-blue">${doc.category}</span>
        </div>
        <div style="font-size: 12px; color: #525252; margin-bottom: 0.4rem;">Source: ${doc.source}</div>
        <p style="font-size: 13px; color: #393939; line-height: 1.5;">${doc.snippet}</p>
      </div>
    `).join('');
  } catch (e) {
    console.error('KB error:', e);
  }
}

async function addCustomKnowledgeDoc() {
  const title = document.getElementById('kb-new-title').value;
  const category = document.getElementById('kb-new-category').value;
  const source = document.getElementById('kb-new-source').value;
  const content = document.getElementById('kb-new-content').value;

  if (!content.trim()) {
    alert('Please enter document content.');
    return;
  }

  try {
    const res = await fetch('/api/knowledge-base/add', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, category, source, content })
    });
    const d = await res.json();
    alert('Document parsed via IBM Docling and vector-indexed with IBM Slate!');
    document.getElementById('kb-new-title').value = '';
    document.getElementById('kb-new-content').value = '';
    loadKnowledgeBase();
  } catch (e) {
    alert('Error adding document: ' + e.message);
  }
}

// ----------------- Settings & watsonx Connection Test ----------------- //

async function loadSettings() {
  try {
    const res = await fetch('/api/settings');
    const s = await res.json();

    document.getElementById('set-watsonx-key').value = s.WATSONX_APIKEY ? '••••••••••••••••' : '';
    document.getElementById('set-watsonx-project').value = s.WATSONX_PROJECT_ID ? '••••••••••••••••' : '';
    document.getElementById('set-watsonx-url').value = s.WATSONX_URL || 'https://us-south.ml.cloud.ibm.com';
    document.getElementById('set-watsonx-model').value = s.WATSONX_MODEL_ID || 'ibm/granite-3-8b-instruct';
    document.getElementById('set-cos-endpoint').value = s.IBM_COS_ENDPOINT || '';
    document.getElementById('set-cos-bucket').value = s.IBM_COS_BUCKET_NAME || '';

    const statBox = document.getElementById('set-connection-status-box');
    const st = s.watsonx_status;
    statBox.innerHTML = `
      <div style="font-size: 13px;">
        <strong>Active Foundation Model:</strong> ${st.foundation_model}<br>
        <strong>Embedding Engine:</strong> ${st.embedding_model}<br>
        <strong>Status:</strong> ${st.mode}<br>
        <strong>Document Parser:</strong> ${st.docling_status}
      </div>
    `;
  } catch (e) {
    console.error('Settings load error:', e);
  }
}

async function saveSettingsData() {
  const payload = {
    WATSONX_URL: document.getElementById('set-watsonx-url').value,
    WATSONX_MODEL_ID: document.getElementById('set-watsonx-model').value,
    IBM_COS_ENDPOINT: document.getElementById('set-cos-endpoint').value,
    IBM_COS_BUCKET_NAME: document.getElementById('set-cos-bucket').value
  };

  const keyInput = document.getElementById('set-watsonx-key').value;
  if (keyInput && !keyInput.includes('••')) {
    payload.WATSONX_APIKEY = keyInput;
  }
  const projInput = document.getElementById('set-watsonx-project').value;
  if (projInput && !projInput.includes('••')) {
    payload.WATSONX_PROJECT_ID = projInput;
  }

  try {
    const res = await fetch('/api/settings', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    });
    const d = await res.json();
    alert('Settings successfully updated!');
    loadSettings();
    loadSystemStatus();
  } catch (e) {
    alert('Error saving settings: ' + e.message);
  }
}

async function testWatsonxConnection() {
  const resultDiv = document.getElementById('test-conn-result');
  resultDiv.innerHTML = `<span style="color: #0f62fe;">Pinging IBM Cloud IAM & watsonx.ai foundation model endpoint...</span>`;

  try {
    const res = await fetch('/api/settings/test', { method: 'POST' });
    const data = await res.json();
    if (data.success) {
      resultDiv.innerHTML = `
        <div style="background: #defbe6; border: 1px solid #24a148; padding: 0.75rem; color: #0e6027; margin-top: 0.5rem;">
          <strong>✓ Connection Verified:</strong> ${data.message}
        </div>
      `;
    } else {
      resultDiv.innerHTML = `
        <div style="background: #ffd7d9; border: 1px solid #da1e28; padding: 0.75rem; color: #a2191f; margin-top: 0.5rem;">
          <strong>Notice (${data.status}):</strong> ${data.message}
        </div>
      `;
    }
  } catch (e) {
    resultDiv.innerHTML = `<div style="color: #da1e28; margin-top: 0.5rem;">Connection test failed: ${e.message}</div>`;
  }
}

// ----------------- Event Listeners ----------------- //

function setupEventListeners() {
  // Navigation buttons inside cards
  document.querySelectorAll('[data-goto]').forEach(btn => {
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      const target = btn.getAttribute('data-goto');
      if (target) navigateTo(target);
    });
  });
}
