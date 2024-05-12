"""athena/llm/research/planner.py"""

import json

from tenacity import retry, stop_after_attempt

from athena.llm.client import groq, openai

PLANNER_SYSTEM_PROMPT = """
You are a scientist working on a research project with a specific task (a small part of a larger research objective).
Your job is to plan the research task using the following skills in the most effective way.

1. web - search the internet for latest information.
2. wiki - search Wikipedia for accurate information.
3. memory - search scientific papers and literature for relevant information, including specific data, methodologies, and findings pertinent to the research question.
4. summarize - provide a technical summary of scientific papers and literature, focusing on key data points, experimental designs, and conclusions that directly address the research task.
5. analyze - analyze the information you have gathered based on a task.
6. write - write about a task using the gathered research to fulfill the task and present to the research team.
7. planner - continue planning the research project using the provided context information.

Your goal is to generate a plan sequentially, considering the complexity of the objective and the available context to determine the most appropriate next task for furthering the understanding of the objective.

If the objective is relatively easy or only requires a simple web/wiki search, call the appropriate agent (e.g., "web" or "wiki") to gather the necessary information.

If the objective requires a more thorough analysis, call the most appropriate agent (e.g., "memory", "summarize", or "analyze") to fill in the missing details.

If enough information is available in the context to answer the objective, request the "write" agent to draft an answer.

You must return the next task in the plan as a JSON object with keys "agent" and "task".

[EXAMPLE]
context: None
task: "How does deforestation affect the biodiversity of the Amazon rainforest?"

assistant: 
{
  "agent": "web",
  "task": "What is the current state of the Amazon rainforest?"
}

context: <Some useful information about the Amazon rainforest and deforestation>
task: "How does deforestation affect the biodiversity of the Amazon rainforest?"

assistant:
{
  "agent": "write",
  "task": "Write a detailed report on the effects of deforestation on the Amazon rainforest."
}

[END EXAMPLE]
""".strip()


@retry(stop=stop_after_attempt(5))
async def planner(task: str, context: str = None) -> dict[str, str]:
    """
    Plan the next research task based on the objective and context information.

    Args:
        task (str): The research objective.
        context (str): The context information to plan the next research task.
    """
    messages = [
        {"role": "system", "content": PLANNER_SYSTEM_PROMPT},
    ]

    if context:
        messages.append({"role": "user", "content": context})

    messages.append({"role": "user", "content": task})

    response = await groq.chat.completions.create(
        model="llama-8b-8192",
        messages=messages,
        response_format={"type": "json_object"},
        temperature=0.2,
    )

    plan = json.loads(response.choices[0].message.content).get("plan", [])

    if len(plan) > 0:
        return plan[0]
    else:
        return {
            "agent": "write",
            "task": "Write a detailed report on the given objective.",
        }


async def research_planner(task: str, context: str = None) -> dict[str, str]:
    """
    Plan the next research task based on the objective and context information.

    Args:
        task (str): The research objective.
        context (str): The context information to plan the next research task.
    """

    messages = [
        {"role": "system", "content": PLANNER_SYSTEM_PROMPT},
    ]

    if context:
        messages.append({"role": "user", "content": context})

    messages.append({"role": "user", "content": task})

    response = await openai.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=messages,
        response_format={"type": "json_object"},
        temperature=0.2,
    )

    plan = json.loads(response.choices[0].message.content).get("plan", [])

    if len(plan) > 0:
        return plan[0]
    else:
        return {
            "agent": "write",
            "task": "Write a detailed report on the given objective.",
        }
