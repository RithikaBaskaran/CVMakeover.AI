import os
from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT", "8000"))
ALLOW_ORIGINS = os.getenv("ALLOW_ORIGINS", "*")

# Optional local LLM (Ollama) — still free
OLLAMA_URL = os.getenv("OLLAMA_URL", "").strip()
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "").strip()
