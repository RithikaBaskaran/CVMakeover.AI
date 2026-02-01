from fastapi import APIRouter
from .models import GenerateRequest, GenerateResponse
from .services.tailor import tailor_profile
from .services.latex import render_latex

router = APIRouter()

@router.post("/generate", response_model=GenerateResponse)
def generate(req: GenerateRequest):
    tailored = tailor_profile(req.profile, req.job_description)
    latex = render_latex(tailored)
    return GenerateResponse(latex=latex)
