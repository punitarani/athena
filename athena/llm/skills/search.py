"""athena/llm/skills/search.py"""

from athena.llm.client import cohere
from athena.llm.embed import embed_text
from athena.store.vector import pc_papers

SEARCH_WEB_PREAMBLE = """
You are a scientist with access to the internet.
Your task is to answer the following question accurately and in extreme detail using web-search.
""".strip()

SEARCH_WIKI_PREAMBLE = """
You are a scientist with access to Wikipedia.
Your task is to answer the following question accurately and in extreme detail using information from Wikipedia.
""".strip()


async def search_web(question: str) -> str:
    """Search the internet for the answer to a question."""

    web_search = await cohere.chat(
        message=question,
        preamble=SEARCH_WEB_PREAMBLE,
        model="command-r",
        connectors=[{"id": "web-search"}],
        temperature=0.2,
        stream=False,
        citation_quality="accurate",
    )
    sources = [document["url"] for document in web_search.documents]
    sources_text = "\n\n".join([f"> {source}" for source in sources])
    return web_search.text + f"\n\n{sources_text}"


async def search_wiki(question: str) -> str:
    """Search Wikipedia for the answer to a question."""

    wiki_search = await cohere.chat(
        message=question,
        preamble=SEARCH_WIKI_PREAMBLE,
        model="command-r",
        connectors=[
            {"id": "web-search", "options": {"site": "https://www.wikipedia.org/"}}
        ],
        temperature=0.2,
        stream=False,
        citation_quality="accurate",
    )
    sources = [document["url"] for document in wiki_search.documents]
    sources_text = "\n\n".join([f"> {source}" for source in sources])
    return wiki_search.text + f"\n\n{sources_text}"


async def search_memory(question: str, n: int = 10) -> str:
    """Search the memory for the answer to a question."""
    q_vector = await embed_text(text=question, input_type="search_query")

    docs = pc_papers.query(
        vector=q_vector,
        top_k=n,
        include_values=False,
        include_metadata=True,
        namespace="papers",
    )

    memory_search = await cohere.chat(
        model="command-r",
        message=question,
        documents=[
            {
                "title": f"[{doc['metadata']['title']}]({doc['metadata']['work_id']})",
                "snippet": doc["metadata"]["text"],
            }
            for doc in docs.get("matches", [])
        ],
        temperature=0.2,
        stream=False,
        citation_quality="accurate",
    )
    sources = [document["title"] for document in memory_search.documents]
    sources_text = "\n\n".join([f"> {source}" for source in sources])
    return memory_search.text + f"\n\n{sources_text}"
