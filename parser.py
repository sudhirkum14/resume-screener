import json
import re
from models import ScreenResult


def extract_json(raw_text: str) -> dict:
    """
    Extracts JSON from LLM response text.
    Handles cases where model wraps response in markdown code blocks.
    """
    # Strip markdown fences if present
    clean = re.sub(r"```(?:json)?", "", raw_text).strip()

    # Try direct parse first
    try:
        return json.loads(clean)
    except json.JSONDecodeError:
        pass

    # Fallback: find first { ... } block
    match = re.search(r"\{.*\}", clean, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass

    raise ValueError(f"Could not extract valid JSON from response:\n{raw_text[:300]}")


def parse_screen_result(raw_text: str) -> ScreenResult:
    """
    Parses and validates raw LLM response into ScreenResult.
    Raises ValueError if parsing or validation fails.
    """
    data = extract_json(raw_text)

    # Validate required fields exist
    required = {"match_score", "strengths", "missing_skills", "recommendation"}
    missing = required - set(data.keys())
    if missing:
        raise ValueError(f"Missing fields in LLM response: {missing}")

    # Coerce types safely
    data["match_score"] = int(data["match_score"])
    data["strengths"] = [str(s) for s in data.get("strengths", [])]
    data["missing_skills"] = [str(s) for s in data.get("missing_skills", [])]
    data["recommendation"] = str(data["recommendation"])

    return ScreenResult(**data)
