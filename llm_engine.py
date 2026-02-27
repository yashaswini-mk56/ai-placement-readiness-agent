import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def analyze_resume(resume_text, company_type):

    prompt = f"""
    You are an expert AI Placement Mentor.

    Analyze this resume:

    {resume_text}

    Target Company Type: {company_type}

    Give structured output:

    Placement Readiness Score (out of 10):
    Missing Skills:
    Interview Questions (5):
    30-Day Roadmap (Week 1–4):
    """

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content