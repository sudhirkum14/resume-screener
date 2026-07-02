"""
Quick test script — run this to verify the API works end to end.
Usage: python test_api.py
Make sure the server is running first: uvicorn main:app --reload
"""

import httpx
import json

BASE_URL = "http://localhost:8000"

JOB_DESCRIPTION = """
We are looking for a Backend Python Developer with experience in:
- FastAPI or Django REST framework
- PostgreSQL and SQL query optimization
- REST API design and development
- Docker and containerization
- Experience with LLMs or AI APIs is a plus
- Git and CI/CD pipelines
- 2+ years of experience
"""

RESUME = """
Kumar - Backend Developer
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
- Async StateTracker pipeline for structured delta extraction from messages
"""


def test_health():
    r = httpx.get(f"{BASE_URL}/health")
    print(f"Health: {r.status_code} — {r.json()}")
    assert r.status_code == 200


def test_screen():
    payload = {"job_description": JOB_DESCRIPTION, "resume": RESUME}
    r = httpx.post(f"{BASE_URL}/screen", json=payload, timeout=40)
    print(f"\nScreen endpoint: {r.status_code}")
    result = r.json()
    print(json.dumps(result, indent=2))
    assert r.status_code == 200
    assert result["success"] is True
    assert 0 <= result["data"]["match_score"] <= 100


if __name__ == "__main__":
    print("=== Testing Resume Screener API ===\n")
    test_health()
    test_screen()
    print("\n✅ All tests passed!")
