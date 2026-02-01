import os
from typing import Optional, List
from groq import Groq

def can_use_groq() -> bool:
    return bool(os.getenv("GROQ_API_KEY"))

def rewrite_bullet_with_groq(
    bullet: str,
    keywords: List[str]
) -> Optional[str]:

    if not can_use_groq():
        return None

    prompt = (
        "Rewrite this resume bullet to strongly match the job keywords. "
        "Be concise, action-oriented, and ATS-friendly.\n\n"
        f"Job keywords: {', '.join(keywords[:10])}\n"
        f"Original bullet: {bullet}\n\n"
        "Return exactly ONE rewritten bullet. No explanations."
    )

    try:
        client = Groq()
        completion = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_completion_tokens=128,
        )

        rewritten = completion.choices[0].message.content.strip()

        # 🔥 HARD PROOF MARKER
        return f"[LLM REWRITE] {rewritten}"

    except Exception as e:
        print("❌ Groq LLM error:", e)
        return None
