import httpx
from config import OPENROUTER_API_KEY, OPENROUTER_BASE_URL, MODEL, REQUEST_TIMEOUT, MAX_TOKENS
from prompts import SYSTEM_PROMPT, build_user_prompt


async def call_openrouter(job_description: str, resume: str) -> str:
    """
    Calls OpenRouter API and returns raw response text.
    Raises httpx.HTTPStatusError on non-2xx responses.
    Raises httpx.TimeoutException on timeout.
    """
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://resume-screener.local",
        "X-Title": "Resume Screener",
    }

    payload = {
        "model": MODEL,
        "max_tokens": MAX_TOKENS,
        "temperature": 0.1,  # Low temp for consistent structured output
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(job_description, resume)},
        ],
    }

    async with httpx.AsyncClient(timeout=REQUEST_TIMEOUT) as client:
        response = await client.post(OPENROUTER_BASE_URL, headers=headers, json=payload)
        response.raise_for_status()

    data = response.json()

    # Extract text from response
    try:
        return data["choices"][0]["message"]["content"]
    except (KeyError, IndexError) as e:
        raise ValueError(f"Unexpected API response structure: {data}") from e
