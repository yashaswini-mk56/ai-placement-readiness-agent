import requests

def analyze_resume(resume_text, company_type):

    prompt = f"""
    You are an expert Placement AI.

    Analyze this resume for {company_type} company:

    {resume_text}

    Provide:
    - Placement Readiness Score (out of 10)
    - Strengths
    - Missing Skills
    - 5 Interview Questions
    - 30-Day Roadmap
    """

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "gemma:7b",
            "prompt": prompt,
            "stream": False
        }
    )

    return response.json()["response"]