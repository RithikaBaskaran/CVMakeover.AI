from typing import List, Optional
from groq import Groq

def rewrite_bullet_with_groq(bullet: str, keywords: List[str]) -> str:
    """
    Always try to rewrite the bullet using Groq LLM.
    If an error occurs, fallback to returning the original bullet.
    """
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
        return rewritten
    except Exception as e:
        print("❌ Groq LLM error:", e)
        return bullet  # fallback to original bullet
