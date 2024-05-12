"""athena/llm/skills/analyze.py"""

from athena.llm.client import openai

ANALYZE_SYSTEM_PROMPT = """
You are a research scientist.
Your task is to analyze the following text and data using the guiding task prompt.
You should provide a detailed and methodical analysis with supporting evidence and reasoning.
""".strip()


async def analyze_texts(texts: list[str], task: str) -> str:
    """
    Analyze the texts using the provided task prompt.

    Args:
        texts (list[str]): Texts to analyze
        task (str): Task prompt

    Returns:
        str: Analysis of the texts
    """

    data = "\n\n".join(texts)
    text = f"{data}\n\n\nUsing the provided data above, analyze the following: {task}"

    response = await openai.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "system", "content": ANALYZE_SYSTEM_PROMPT},
            {"role": "user", "content": text},
        ],
        response_format={"type": "text"},
        temperature=0,
    )

    return response.choices[0].message.content
