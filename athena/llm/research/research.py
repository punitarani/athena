"""athena/llm/research/research.py"""

from athena.llm.skills import (
    analyze_texts,
    search_memory,
    search_web,
    search_wiki,
    summarize_papers,
    write,
)


async def run_agent(agent: str, prompt: str, context: str | list[str]) -> str:
    """Execute the task using the agent."""
    if agent == "analyze":
        return await analyze_texts(task=prompt, texts=context)

    if agent == "research":
        return await search_memory(question=prompt, n=10)

    if agent == "web":
        return await search_web(question=prompt)

    if agent == "wiki":
        return await search_wiki(question=prompt)

    if agent == "papers":
        return await summarize_papers(topic=prompt)

    if agent == "write":
        return await write(task=prompt, texts=context)
