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
    llm_rewrites = 0

    for section in ["experience", "projects"]:
        for item in tailored.get(section, []):
            new_bullets = []
            for b in item.get("bullets", []):
                rb = rewrite_bullet_with_groq(b, keywords)
                if rb:
                    llm_rewrites += 1
                    new_bullets.append(rb)
                else:
                    new_bullets.append(b)
            item["bullets"] = new_bullets

    print(f"🧠 Total bullets rewritten by LLM: {llm_rewrites}")

    latex = render_latex(tailored)
    return GenerateResponse(latex=latex)
