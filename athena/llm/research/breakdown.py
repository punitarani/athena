"""
athena/llm/research/breakdown.py

In order to fulfill broad research objective, you need to:
1. conduct background research to identify what exactly needs to be done
2. break down the research objective into smaller tasks
"""

import json

from athena.llm.client import groq, openai

BREAKDOWN_SYSTEM_PROMPT = """
You are a scientist working on a research project.
You are trying to break down a complex scientific research idea into simpler components.
You need to break down the idea into smaller, more manageable parts.
You need to understand the different aspects of the idea and how they relate to each other.

All the steps should be exploratory research through previous experiments and literature review.
Do not include any steps that requires conducting new experiments or collecting new data.
It should be a logical progression of steps that build on each other and lead to a conclusion.

Each step should be very clear and should not require any further explanation or context.
The step should be very specific and should not be too broad or general.

List the different steps in logical order in JSON format.
It should have a single root key "steps" and a list of strings as the value.
""".strip()


async def breakdown(objective: str) -> list[str]:
    """Break down a complex scientific research objective into smaller research tasks."""

    response = await groq.chat.completions.create(
        model="llama-8b-8192",
        messages=[
            {"role": "system", "content": BREAKDOWN_SYSTEM_PROMPT},
            {"role": "user", "content": objective},
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )
    return json.loads(response.choices[0].message.content).get("steps", [])


async def breakdown_objective(objective: str) -> list[str]:
    """Break down a complex scientific research objective into smaller research tasks."""

    response = await openai.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": BREAKDOWN_SYSTEM_PROMPT},
            {"role": "user", "content": objective},
        ],
        response_format={"type": "json_object"},
        temperature=0,
    )
    return json.loads(response.choices[0].message.content).get("steps", [])
