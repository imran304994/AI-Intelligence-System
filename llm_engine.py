from groq import Groq
from utils import safe_json_loads, normalize_score

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))


def analyze_resume_general(resume_text):

    prompt = f"""
    You are an AI Resume Analyzer.

    Evaluate the resume professionally like an ATS system.

    Return STRICT JSON:

    {{
        "skills": [],
        "experience": "",
        "best_role": "",
        "resume_score": 0,
        "ats_score": 0,
        "strengths": [],
        "weaknesses": [],
        "suggestions": []
    }}

    Rules:
    - Scores must be between 0–100
    - Keep suggestions short and actionable
    - Do NOT add explanation outside JSON

    Resume:
    {resume_text}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    data = safe_json_loads(response.choices[0].message.content)

    data["resume_score"] = normalize_score(data.get("resume_score"))
    data["ats_score"] = normalize_score(data.get("ats_score"))

    return data


def analyze_role_match(resume_text, target_role):

    prompt = f"""
    You are an AI Hiring System.

    Compare resume with role: {target_role}

    Return STRICT JSON:

    {{
        "match_percentage": 0,
        "matching_skills": [],
        "missing_skills": [],
        "reason": "",
        "improvement_suggestions": []
    }}

    Rules:
    - Score must be realistic (not always high)
    - Missing skills must be relevant to role
    - Keep reason 1–2 lines only

    Resume:
    {resume_text}
    """

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    data = safe_json_loads(response.choices[0].message.content)

    data["match_percentage"] = normalize_score(data.get("match_percentage"))

    return data
