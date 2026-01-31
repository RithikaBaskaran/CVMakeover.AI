from fastapi import APIRouter
from .models import GenerateRequest, GenerateResponse
from .services.tailor import tailor_profile
from .services.latex import render_latex
from .services.llm_optional import rewrite_bullet_with_ollama

router = APIRouter()

@router.post("/generate", response_model=GenerateResponse)
def generate(req: GenerateRequest):
  tailored = tailor_profile(req.profile, req.job_description)

  # Optional: if Ollama configured, try rewriting a few bullets
  # (still works even if not configured)
  keywords = tailored.get("jd_keywords", [])
  for section in ["experience", "projects"]:
    for item in tailored.get(section, []):
      new_bullets = []
      for b in item.get("bullets", []):
        rb = rewrite_bullet_with_ollama(b, keywords)
        new_bullets.append(rb if rb else b)
      item["bullets"] = new_bullets

  latex = render_latex(tailored)
  return GenerateResponse(latex=latex)
