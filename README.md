# Smart Resume Screener API

AI-powered resume screening using FastAPI + OpenRouter (LLaMA 3.3 70B).

## Project Structure

```
resume-screener/
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── models.py
│   ├── prompts.py
│   ├── api_client.py
│   ├── parser.py
│   └── requirements.txt
└── frontend/
    ├── index.html
    ├── style.css
    └── script.js
```

## Setup

```bash
# 1. Create virtual environment
python -m venv myenv
# Windows PowerShell:
myenv\Scripts\Activate.ps1
# Windows CMD:
myenv\Scripts\activate.bat
# macOS/Linux:
source myenv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your API key
# Create or update .env in the project root with:
# OPENROUTER_API_KEY=your-real-openrouter-key

# 4. Run the server
uvicorn main:app --reload
```

## API Usage

### POST /screen

```bash
curl -X POST http://localhost:8000/screen \
  -H "Content-Type: application/json" \
  -d '{
    "job_description": "We need a Python backend developer with FastAPI, PostgreSQL...",
    "resume": "John Doe — 3 years Python experience, built REST APIs with FastAPI..."
  }'
```

### Response

```json
{
  "success": true,
  "data": {
    "match_score": 78,
    "strengths": ["FastAPI", "PostgreSQL", "REST API design"],
    "missing_skills": ["Docker", "CI/CD", "Redis"],
    "recommendation": "Strong backend candidate — recommend interview, address DevOps gaps."
  }
}
```

## Interactive Docs

Visit `http://localhost:8000/docs` for Swagger UI after starting the server.

## Test

```bash
# Make sure server is running first
python test_api.py
```

## Deploy to Railway

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login and deploy
railway login
railway init
railway up
```

Add `OPENROUTER_API_KEY` as an environment variable in Railway dashboard.
