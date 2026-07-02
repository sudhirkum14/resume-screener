import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from models import ScreenRequest, ScreenResponse
from api_client import call_openrouter
from parser import parse_screen_result

app = FastAPI(
    title="Smart Resume Screener API",
    description="AI-powered resume screening using LLMs via OpenRouter",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"status": "ok", "message": "Resume Screener API is running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/screen", response_model=ScreenResponse)
async def screen_resume(request: ScreenRequest):
    """
    Screen a resume against a job description.
    Returns match score, strengths, missing skills, and a hiring recommendation.
    """
    try:
        raw_response = await call_openrouter(request.job_description, request.resume)
        result = parse_screen_result(raw_response)
        return ScreenResponse(success=True, data=result)

    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="LLM API request timed out. Try again.")

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=502,
            detail=f"OpenRouter API error: {e.response.status_code} - {e.response.text[:200]}",
        )

    except ValueError as e:
        raise HTTPException(status_code=422, detail=f"Response parsing failed: {str(e)}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")
