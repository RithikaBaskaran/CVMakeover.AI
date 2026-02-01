from groq import Groq

def rewrite_bullet_with_groq(bullet: str, job_description: str) -> str:
    """
    Rewrite a resume bullet using Groq LLM.
    Receives the full job description as input for better relevance.
    """
    prompt = (
        "Rewrite this resume bullet to strongly match the job keywords. "
        "Be concise, action-oriented, and ATS-friendly.\n\n"
        f"Job keywords: {job_description}\n"
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
        # fallback if LLM fails
        return f"[LLM FAILED] {bullet}"
