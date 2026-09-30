"""Shared model configuration for EduGenie.

Every feature module talks to the model through generate_text() at the bottom of
this file, so the provider, model name and credentials live in exactly one place.

Gemini is the default provider, so the project stays Gemini-first. Set
LLM_PROVIDER=openai in .env to run the same five features on an OpenAI-compatible
endpoint instead (OpenAI itself, or any compatible gateway).
"""
import os
import time

from dotenv import load_dotenv

# Load .env, which sits next to this module. override=True makes this file the
# source of truth, so a stale machine-level GEMINI_API_KEY cannot silently
# shadow the key you put here.
load_dotenv(override=True)

GEMINI = "gemini"
OPENAI = "openai"

# --- Which provider is active ----------------------------------------------
_requested_provider = (os.getenv("LLM_PROVIDER") or GEMINI).strip().lower()
LLM_PROVIDER = _requested_provider if _requested_provider in (GEMINI, OPENAI) else GEMINI
PROVIDER_LABEL = "Gemini" if LLM_PROVIDER == GEMINI else "OpenAI"

# --- Gemini settings (the default provider) --------------------------------
# The old "gemini-1.5-*" and "gemini-2.0-*" models are shut down, so default to
# a current stable GA model. gemini-3.6-flash is used in preference to the newer
# gemini-3.8-flash because the newest models frequently return
# 429 RESOURCE_EXHAUSTED on a free-tier key. Override via GEMINI_MODEL in .env.
GEMINI_MODEL = os.getenv("GEMINI_MODEL") or "gemini-3.6-flash"

# --- OpenAI-compatible settings (the optional provider) --------------------
# OPENAI_BASE_URL also lets you point at any OpenAI-compatible gateway.
OPENAI_MODEL = os.getenv("OPENAI_MODEL") or "gpt-4o-mini"
OPENAI_BASE_URL = (os.getenv("OPENAI_BASE_URL") or "https://api.openai.com/v1").rstrip("/")

# --- The key and model actually in use -------------------------------------
KEY_ENV_VAR = "GEMINI_API_KEY" if LLM_PROVIDER == GEMINI else "OPENAI_API_KEY"
KEY_SETUP_URL = (
    "https://aistudio.google.com/apikey"
    if LLM_PROVIDER == GEMINI
    else "https://platform.openai.com/api-keys"
)
MODEL_IN_USE = GEMINI_MODEL if LLM_PROVIDER == GEMINI else OPENAI_MODEL

_gemini_client = None


def get_api_key():
    """Return the API key for the active provider, or None when it is missing."""
    key = os.getenv(KEY_ENV_VAR)
    return key.strip() if key else None


def _generate_with_gemini(prompt: str) -> str:
    """Call the Gemini API through the google-genai SDK."""
    global _gemini_client

    if _gemini_client is None:
        # Imported here so the OpenAI path needs no Google SDK installed.
        from google import genai

        _gemini_client = genai.Client(api_key=get_api_key())

    response = _gemini_client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
    )
    return response.text


def _generate_with_openai(prompt: str) -> str:
    """Call any OpenAI-compatible /chat/completions endpoint."""
    import httpx

    response = httpx.post(
        OPENAI_BASE_URL + "/chat/completions",
        headers={
            "Authorization": "Bearer " + (get_api_key() or ""),
            "Content-Type": "application/json",
        },
        json={
            "model": OPENAI_MODEL,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=120,
    )
    if response.status_code != 200:
        raise RuntimeError(
            f"endpoint returned HTTP {response.status_code}: {response.text[:300]}"
        )
    return response.json()["choices"][0]["message"]["content"]


# Both providers report a rejected key, just with different wording.
_INVALID_KEY_MARKERS = (
    "api_key_invalid",
    "api key not valid",
    "incorrect api key",
    "invalid_api_key",
)

# A model that is momentarily overloaded (503) or briefly over quota (429) is
# worth another attempt; these are common on the Gemini free tier and usually
# clear within seconds.
_TRANSIENT_MARKERS = (
    "503",
    "unavailable",
    "429",
    "resource_exhausted",
    "overloaded",
)
_RETRY_ATTEMPTS = 3
_RETRY_WAIT_SECONDS = 2


def _is_transient(exc: Exception) -> bool:
    """True when the failure looks like a temporary capacity/quota spike."""
    text = str(exc).lower()
    return any(marker in text for marker in _TRANSIENT_MARKERS)


def _readable_error(exc: Exception) -> Exception:
    """Rewrite a rejected key or a busy model as an actionable message."""
    text = str(exc).lower()
    if any(marker in text for marker in _INVALID_KEY_MARKERS):
        return RuntimeError(
            f"{PROVIDER_LABEL} rejected {KEY_ENV_VAR} as invalid. "
            f"Create a key at {KEY_SETUP_URL} and update it in EduGenie/.env."
        )
    if _is_transient(exc):
        return RuntimeError(
            f"{PROVIDER_LABEL} is temporarily busy (the model is overloaded or the "
            "quota is briefly exhausted). Please try this again in a few seconds."
        )
    return exc


def generate_text(prompt: str) -> str:
    """Send a single prompt to the active provider and return the plain-text reply.

    Transient capacity/quota spikes are retried a couple of times before giving up.
    """
    if not get_api_key():
        raise RuntimeError(
            f"{KEY_ENV_VAR} is missing. Add it to EduGenie/.env "
            f"(create a key at {KEY_SETUP_URL})."
        )

    last_error = None
    for attempt in range(1, _RETRY_ATTEMPTS + 1):
        try:
            if LLM_PROVIDER == GEMINI:
                return _generate_with_gemini(prompt)
            return _generate_with_openai(prompt)
        except Exception as exc:
            last_error = exc
            if attempt < _RETRY_ATTEMPTS and _is_transient(exc):
                time.sleep(_RETRY_WAIT_SECONDS * attempt)
                continue
            break

    readable = _readable_error(last_error)
    if readable is last_error:
        raise last_error
    raise readable from last_error
