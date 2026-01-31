from pydantic import BaseModel

class ResumeRequest(BaseModel):
    profile: dict
    job_description: str
