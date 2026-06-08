from google import genai
from config import GEMINI_API_KEY

client = genai.Client(api_key=GEMINI_API_KEY)


def get_resume_feedback(resume_text, job_description):

    prompt = f"""
    You are an ATS and career advisor.

    Resume:
    {resume_text}

    Job Description:
    {job_description}

    Give:
    1. ATS Evaluation
    2. Missing Skills
    3. Resume Improvement Suggestions

    Keep the response concise.
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )

    return response.text