from pydantic import BaseModel, Field
from typing import List


class ScreenRequest(BaseModel):
    job_description: str = Field(..., min_length=50, description="Full job description text")
    resume: str = Field(..., min_length=50, description="Resume text")


class ScreenResult(BaseModel):
    match_score: int = Field(..., ge=0, le=100, description="Match score 0–100")
    strengths: List[str] = Field(..., description="Matching skills and positives")
    missing_skills: List[str] = Field(..., description="Skills in JD but absent in resume")
    recommendation: str = Field(..., description="One-line hiring recommendation")


class ScreenResponse(BaseModel):
    success: bool
    data: ScreenResult | None = None
    error: str | None = None
