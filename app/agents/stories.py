import json
from ..llm import get_llm


def stories_agent(requirements: dict, inception: dict):

    llm = get_llm()

    prompt = f"""
You are an agile analyst.

Based on the requirements and inception document, generate user stories.

Each story must include:

- id (US-001)
- title
- description
- acceptance_criteria
- related_requirements (REQ-xxx)

Return ONLY valid JSON:

{{
  "stories": [
    {{
      "id": "US-001",
      "title": "...",
      "description": "...",
      "acceptance_criteria": "...",
      "related_requirements": ["REQ-001"]
    }}
  ]
}}

Requirements:
{requirements}

Inception:
{inception}
"""

    response = llm.invoke(prompt)

    content = response.content.strip()

    if content.startswith("```"):
        content = content.replace("```json", "").replace("```", "").strip()

    return json.loads(content)
