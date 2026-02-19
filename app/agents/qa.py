import json
from ..llm import get_llm


def qa_agent(stories: dict):

    llm = get_llm()

    prompt = f"""
You are a QA engineer.

Based on the following user stories, generate test cases.

Each test case must include:

- id (TC-001)
- description
- steps
- expected_result
- related_story (US-xxx)

Return ONLY valid JSON:

{{
  "test_cases": [
    {{
      "id": "TC-001",
      "description": "...",
      "steps": "...",
      "expected_result": "...",
      "related_story": "US-001"
    }}
  ]
}}

Stories:
{stories}
"""

    response = llm.invoke(prompt)

    content = response.content.strip()

    if content.startswith("```"):
        content = content.replace("```json", "").replace("```", "").strip()

    # fallback si no es JSON
    if not content.startswith("{"):
        raise ValueError(f"Invalid JSON from model: {content[:200]}")

    return json.loads(content)
