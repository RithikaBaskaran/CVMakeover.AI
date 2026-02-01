!pip install groq

import os
from typing import Optional, List
from groq import Groq

def can_use_groq() -> bool:
    return bool(os.getenv("GROQ_API_KEY"))

def rewrite_bullet_with_groq(
    bullet: str,
    keywords: List[str]
) -> Optional[str]:
    """
    Rewrite resume bullet using Groq (LLaMA 3.1).
    Returns None if Groq is not configured or fails.
    """

    if not can_use_groq():
        return None

    prompt = (
        "Rewrite the following resume bullet to better match the job keywords, "
        "while staying strictly truthful.\n\n"
        f"Job keywords: {', '.join(keywords[:15])}\n"
        f"Original bullet: {bullet}\n\n"
        "Return exactly ONE improved bullet. "
        "Concise, action-oriented, ATS-friendly. No explanations."
    )

    try:
        client = Groq()
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.5,
            max_completion_tokens=128,
            top_p=1,
        )
        return completion.choices[0].message.content.strip() or None
    except Exception:
        return None
