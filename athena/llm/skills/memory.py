"""athena/llm/skills/memory.py"""

from athena.llm.client import groq
from athena.llm.embed import embed_text
from athena.store.vector import pc_papers


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

    # Create a string of papers
    papers = [
        f"{doc['metadata']['title']}\n{doc['metadata']['text']}"
        for doc in docs["matches"]
    ]

    # Create a response from the LLM model
    response = groq.chat.completions.create(
        model="llama-8b-8192",
        messages=[
            {
                "role": "system",
                "content": "Search the memory for the answer to a question.",
            },
            {"role": "user", "content": question},
            {"role": "system", "content": "Here are some relevant papers:"},
            {"role": "system", "content": "\n\n".join(papers)},
        ],
    )

    return response.messages[-1].content
