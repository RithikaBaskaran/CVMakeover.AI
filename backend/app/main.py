from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import ALLOW_ORIGINS
from .routes import router

app = FastAPI(title="CVMakeover.AI Backend")

# For hackathon: allow local extension/dev
origins = ["*"] if ALLOW_ORIGINS == "*" else [ALLOW_ORIGINS]

app.add_middleware(
  CORSMiddleware,
  allow_origins=origins,
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(router)
