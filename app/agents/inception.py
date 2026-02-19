import json
from ..llm import get_llm


def inception_agent(requirements: dict):

    llm = get_llm()

    prompt = f"""
You are a product manager.

Based on the following requirements, create an inception document.

Include:

- Problem statement
- MVP scope
- Risks
- Assumptions
- Success metrics

Return ONLY valid JSON:

{{
  "inception": {{
    "problem": "...",
    "mvp_scope": "...",
    "risks": "...",
    "assumptions": "...",
    "metrics": "..."
  }}
}}

Requirements:
{requirements}
"""

    response = llm.invoke(prompt)

    content = response.content.strip()

    if content.startswith("```"):
        content = content.replace("```json", "").replace("```", "").strip()

    # fallback si no es JSON
    if not content.startswith("{"):
        raise ValueError(f"Invalid JSON from model: {content[:200]}")

    return json.loads(content)
