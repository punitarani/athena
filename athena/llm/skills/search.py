"""athena/llm/skills/search.py"""

from athena.llm.client import cohere
from athena.llm.embed import embed_text
from athena.store.vector import pc_papers

SEARCH_WEB_PREAMBLE = """
You are a scientist with access to the internet.
Your task is to answer the following question concisely and accurately using web-search.
""".strip()

SEARCH_WIKI_PREAMBLE = """
You are a scientist with access to Wikipedia.
Your task is to answer the following question concisely and accurately using information from Wikipedia.
""".strip()


async def search_web(question: str) -> str:
    """Search the internet for the answer to a question."""

    prediction = await cohere.chat(
        message=question,
        preamble=SEARCH_WEB_PREAMBLE,
        model="command-r-plus",
        temperature=0.2,
        stream=False,
        citation_quality="accurate",
        connectors=[{"id": "web-search"}],
        documents=[],
    )
    return prediction.text


async def search_wiki(question: str) -> str:
    """Search Wikipedia for the answer to a question."""

    prediction = await cohere.chat(
        message=question,
        preamble=SEARCH_WIKI_PREAMBLE,
        model="command-r-plus",
        temperature=0.2,
        stream=False,
        citation_quality="accurate",
        connectors=[
            {"id": "web-search", "options": {"site": "https://www.wikipedia.org/"}}
        ],
        documents=[],
    )
    return prediction.text


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

    chat = await cohere.chat(
        model="command-r-plus",
        message=question,
        documents=[
            {"title": str(doc["metadata"]["doi"]), "snippet": doc["metadata"]["text"]}
            for doc in docs.get("matches", [])
        ],
        temperature=0.2,
    )

    return chat.text
