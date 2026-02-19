import json
from ..llm import get_llm


def design_agent(requirements: dict, stories: dict, testcases: dict):

    llm = get_llm()

    prompt = f"""
        You are a senior software architect.

        Based on the following project artifacts, generate system diagrams in Mermaid syntax.

        Artifacts:

        Requirements:
        {json.dumps(requirements, indent=2)}

        User Stories:
        {json.dumps(stories, indent=2)}

        Test Cases:
        {json.dumps(testcases, indent=2)}

        Generate:

        1. Entity Relationship Diagram (erDiagram)
        2. Sequence Diagram (sequenceDiagram)

        Return ONLY valid JSON:

        {{
        "er": "mermaid code",
        "sequence": "mermaid code"
        }}

        Rules:

        - ER must reflect business entities from requirements.
        - Sequence must reflect a core user flow from stories.
        - Use realistic architecture components.
        - Do NOT include explanations.
        - Only JSON.
"""

    response = llm.invoke(prompt)

    content = response.content.strip()

    if content.startswith("```"):
        content = content.replace("```json", "").replace("```", "").strip()

    # fallback si no es JSON
    if not content.startswith("{"):
        raise ValueError(f"Invalid JSON from model: {content[:200]}")

    return json.loads(content)
