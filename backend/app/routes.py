from fastapi import APIRouter
from .models import GenerateRequest, GenerateResponse
from .services.tailor import tailor_profile
from .services.latex import render_latex
from .services.llm_optional import rewrite_bullet_with_groq

router = APIRouter()

@router.post("/generate", response_model=GenerateResponse)
def generate(req: GenerateRequest):
    tailored = tailor_profile(req.profile, req.job_description)

    keywords = tailored.get("jd_keywords", [])

    #for item in tailored.get("projects", []):
    #    forced_bullets = []
    #    for b in item.get("bullets", []):
    #        print("✏️ Sending bullet to LLM:", b)
    #        rb = rewrite_bullet_with_groq(b, keywords)
    #        forced_bullets.append(rb if rb else b)
    #    item["bullets"] = forced_bullets

    latex = render_latex(tailored)
    return GenerateResponse(latex=latex)
