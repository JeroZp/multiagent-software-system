import json
from ..llm import get_llm


def requirements_agent(brief: str, feedback: str = None):

    llm = get_llm()

    prompt = f"""
    You are a senior business analyst.

    Generate software requirements from this brief.

    """

    if feedback:
        prompt += f"""
    Human feedback to incorporate:
    {feedback}
    """

    prompt += f"""
    Brief:
    {brief}

    Return ONLY valid JSON...



    Structure:

    {{
    "requirements": [
        {{
        "id": "REQ-001",
        "title": "...",
        "description": "...",
        "priority": "High"
        }}
    ]
    }}

    Brief:
    {brief}
    """

    response = llm.invoke(prompt)

    content = response.content.strip()

    if content.startswith("```"):
        content = content.replace("```json", "").replace("```", "").strip()

    # fallback si no es JSON
    if not content.startswith("{"):
        raise ValueError(f"Invalid JSON from model: {content[:200]}")

    return json.loads(content)
