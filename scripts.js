const SAMPLE_JD = `We are looking for a Backend Python Developer with experience in:
- FastAPI or Django REST framework
- PostgreSQL and SQL query optimization
- REST API design and development
- Docker and containerization
- Experience with LLMs or AI APIs is a plus
- Git and CI/CD pipelines
- 2+ years of experience`;

const SAMPLE_RESUME = `Kumar - Backend Developer
Experience: 2 years as Data Analyst + AI Developer

Skills:
- Python (advanced): asyncio, httpx, FastAPI (learning)
- SQL: Snowflake, PostgreSQL, complex query optimization with CTEs and window functions
- AI/NLP: OpenRouter API, Groq, LLM prompt engineering, JSON parsing pipelines
- Tools: Git, GitHub, Docker (basic), REST APIs
- Async programming: ThreadPoolExecutor, asyncio.gather, semaphores

Projects:
- Built celebrity NER pipeline using LLMs with parallel processing
- Benchmarking system for comparing multiple LLMs with precision/recall/F1 metrics
- Async StateTracker pipeline for structured delta extraction from messages`;

const jdE1 = document.getElementById('job-description');
const resumeE1 = document.getElementById('resume');
const jdCount = document.getElementById('jd-count');
const resumeCount = document.getElementById('resume-count');
const apiUrlEl = document.getElementById('api-url');
const apiStatusEl = document.getElementById('api-status');

jdE1.addEventListener('input', () => {
  jdCount.textContent = jdE1.value.length;
});

resumeE1.addEventListener('input', () => {
  resumeCount.textContent = resumeE1.value.length;
});

function loadSample(type) {
  if (type === 'jd') {
    jdE1.value = SAMPLE_JD;
    jdCount.textContent = SAMPLE_JD.length;

  }
  else {
    resumeE1.value = SAMPLE_RESUME;
    resumeCount.textContent = SAMPLE_RESUME.length;
  }
}

async function checkApiHealth() {
  try {
    const res = await fetch(`${apiUrlEl.value}/health`);
    apiStatusEl.className = res.ok ? 'api-status online' : 'api-status offline';
  }
  catch {
    apiStatusEl.className = 'api-status offline';
  }
}

checkApiHealth();
apiUrlEl.addEventListener('change', checkApiHealth);

function showError(msg) {
  const errorBox = document.getElementById('error-box');
  errorBox.textContent = msg;
  errorBox.style.display = 'block';
}

function hideError() {
  document.getElementById('error-box').style.display = 'none';
}

function getScoreClass(score) {
  if (score >= 70) return 'high';
  if (score >= 40) return 'mid';
  return 'low';
}

async function screenResume() {
  const jd = jdE1.value.trim();
  const resume = resumeE1.value.trim()
  const btn = document.getElementById('screen-btn');
  const loading = document.getElementById('loading');
  const resultSection = document.getElementById('result-section');
  hideError();

  if (jd.length < 50) {
    showError('job description must be atleast 50 characters.');
    return;
  }
  if (resume.length < 50) {
    showError('Resume must be at least 50 characters');
    return;
  }

  btn.disabled = true;
  btn.textContent = 'Screening...';
  loading.style.display = 'block';
  resultSection.style.display = 'none';

  try {
    const res = await fetch(`${apiUrlEl.value}/screen`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ job_description: jd, resume: resume }),
    });

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.detail || 'Something went wrong on the server.');
    }

    if (!data.success || !data.data) {
      throw new Error(data.error || 'No result returned from API.');
    }

    renderResult(data.data);
  } catch (err) {
    showError(err.message || 'Failed to connect to the API. Is the server running?');
  } finally {
    btn.disabled = false;
    btn.textContent = 'Screen resume';
    loading.style.display = 'none';
  }
}

function renderResult(result) {
  const scoreCircle = document.getElementById('score-circle');
  scoreCircle.textContent = result.match_score;
  scoreCircle.className = `score-circle ${getScoreClass(result.match_score)}`;

  document.getElementById('recommendation').textContent = result.recommendation;

  const strengthsEl = document.getElementById('strengths-tags');
  strengthsEl.innerHTML = result.strengths.length
    ? result.strengths.map(s => `<span class="tag strength">${escapeHtml(s)}</span>`).join('')
    : '<span style="color:#999;font-size:13px;">None identified</span>';

  const missingEl = document.getElementById('missing-tags');
  missingEl.innerHTML = result.missing_skills.length
    ? result.missing_skills.map(s => `<span class="tag missing">${escapeHtml(s)}</span>`).join('')
    : '<span style="color:#999;font-size:13px;">No major gaps found</span>';

  document.getElementById('result-section').style.display = 'block';
  document.getElementById('result-section').scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

function escapeHtml(str) {
  const div = document.createElement('div');
  div.textContent = str;
  return div.innerHTML;
}