from pydantic import BaseModel
from typing import Any, Dict

class GenerateRequest(BaseModel):
    profile: Dict[str, Any]
    job_description: str

class GenerateResponse(BaseModel):
    latex: str
