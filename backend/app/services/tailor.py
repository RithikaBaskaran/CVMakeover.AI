from app.services.extract import extract_jd
from app.services.latex import render_latex

def tailor_resume(profile: dict, jd: str):
    extracted = extract_jd(jd)
    latex = render_latex(profile, extracted)
    return {"latex": latex}
