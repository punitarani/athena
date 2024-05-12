"""athena/llm/skills/summarize.py"""

import asyncio
from collections import Counter

from athena.llm.client import cohere
from athena.llm.embed import embed_texts
from athena.openalex.download import get_paper_text
from athena.openalex.work import Work, WorkObject
from athena.store.vector import pc_papers


async def summarize_papers(topic: str, n: int = 5) -> str:
    """
    Summarize the texts on the given topic.

    Args:
        topic (str): Topic of the texts
        n (int): Maximum number of texts to summarize

    Returns:
        str: Summary of the texts
    """

    chat_response = await cohere.chat(
        message=topic, model="command-r-plus", search_queries_only=True
    )
    search_queries = [query["text"] for query in chat_response.search_queries]

    q_vectors = await embed_texts(texts=search_queries, input_type="search_query")

    work_ids = []
    for q_vector in q_vectors:
        docs = pc_papers.query(
            vector=q_vector,
            top_k=5,
            include_values=False,
            include_metadata=False,
            namespace="papers",
        )
        matches = docs.get("matches", [])

        # Iterate through the matches' id's
        # id format: work_id#idx
        work_ids.extend([match["id"].split("#")[0] for match in matches])

    # Get the n most common work_id's
    work_ids = [work_id for work_id, _ in Counter(work_ids).most_common(n)]

    works: list[WorkObject] = [
        await Work(entity_id=work_id).get() for work_id in work_ids
    ]

    texts: dict[str, str] = {work.id: await get_paper_text(work=work) for work in works}

    # Asynchronously summarize the texts
    summaries = await asyncio.gather(
        *(summarize_text(text=text) for work_id, text in texts.items())
    )

    return "\n\n\n\n".join(
        f"[{works[i].title}]({works[i].id})\n\n{summary}"
        for i, summary in enumerate(summaries)
    )


async def summarize_text(text: str) -> str:
    """
    Summarize the contents of a research paper.

    Args:
        text (str): Contents of the paper

    Returns:
        str: Summary of the paper
    """

    response = await cohere.chat(
        message=text,
        model="command-r",
        temperature=0.2,
        preamble="Summarize the following research paper in detail.",
    )
    return response.text
