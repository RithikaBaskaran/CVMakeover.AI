import requests
from typing import Optional
from ..config import OLLAMA_URL, OLLAMA_MODEL

def can_use_ollama() -> bool:
  return bool(OLLAMA_URL and OLLAMA_MODEL)

def rewrite_bullet_with_ollama(bullet: str, keywords: list[str]) -> Optional[str]:
  """
  Optional: rewrite bullet with local Ollama model (free).
  If Ollama isn't configured, return None.
  """
  if not can_use_ollama():
    return None

  prompt = (
    "Rewrite this resume bullet to better match the job keywords, while staying truthful.\n"
    f"Job keywords: {', '.join(keywords[:15])}\n"
    f"Bullet: {bullet}\n"
    "Return ONE improved bullet, concise, action-oriented, ATS-friendly."
  )

  try:
    r = requests.post(
      f"{OLLAMA_URL}/api/generate",
      json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
      timeout=20
    )
    r.raise_for_status()
    data = r.json()
    return (data.get("response") or "").strip() or None
  except Exception:
    return None
