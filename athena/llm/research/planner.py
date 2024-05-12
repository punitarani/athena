"""
athena/llm/agents/research/planner.py

Given a particular task, as part of a larger research objective:
the planner splits the task into smaller sub-tasks,
each of which can be assigned to a specialized agent.
"""

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


If you are provided context information, and further research needs to be done, you should return a list of tasks to gather more information and continue planning the research project.
If you are provided context information,and the gathered research IS sufficient to fulfill the task, you should return a single task with the "write" agent to write a detailed report on the task.


You must return the plan in JSON format with a single root key "plan" and a list of tasks with keys "agent" and "task".


[EXAMPLE]
context: None
task: "How does deforestation affect the biodiversity of the Amazon rainforest?"

assistant:
{
  "plan": [
    {
      "agent": "web",
      "task": "What is the current state of the Amazon rainforest?"
    },
    {
      "agent": "wiki",
      "task": "What is a carbon sink?"
    },
    {
      "agent": "memory",
      "task": "Quantify the impact of deforestation on species richness, abundance, and ecosystem services in the Amazon rainforest."
    },
    {
      "agent": summarize",
      "task": "Studies on deforestation and biodiversity loss in the Amazon, including specific data on species decline, habitat fragmentation, and changes in ecosystem functioning."
    },
    {
      "agent": "analyze",
      "task": "Analyze the effects of deforestation on the Amazon rainforest."
    },
    {
      "agent": "planner",
      "task": "Continue planning the research project using the provided context information."
    }
  ]
}


context: <Some useful information about the Amazon rainforest and deforestation>
task: "How does deforestation affect the biodiversity of the Amazon rainforest?"

assistant:
{
  "plan": [
      {
      "agent": "write",
      "task": "Write a detailed report on the effects of deforestation on the Amazon rainforest."
    }
  ]
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


async def research_planner(task: str, context: str = None) -> list[dict[str, str]]:
    """
    Plan the research project based on the task and context information.

    Args:
        task (str): The research task.
        context (str): The context information to plan the research project.
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

    return json.loads(response.choices[0].message.content).get("plan", [])
