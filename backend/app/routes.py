from fastapi import APIRouter
from app.models import ResumeRequest
from app.services.tailor import tailor_resume

router = APIRouter()

@router.post("/tailor")
def tailor(req: ResumeRequest):
    return tailor_resume(req.profile, req.job_description)
