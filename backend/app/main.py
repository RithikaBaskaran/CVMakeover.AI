from fastapi import FastAPI
from app.routes import router

app = FastAPI(title="CVMakeover.AI Backend")

app.include_router(router)

@app.get("/")
def root():
    return {"status": "Backend running"}
