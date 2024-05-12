"""athena/llm/skills/summarize.py"""

import asyncio
from collections import Counter

from langchain.chains import AnalyzeDocumentChain
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import ChatOpenAI

from athena.llm.client import cohere
from athena.llm.embed import embed_texts
from athena.openalex.download import get_paper_text
from athena.openalex.work import Work, WorkObject
from athena.store.vector import pc_papers

SUMMARIZE_PAPER_SYSTEM_PROMPT = """
You will be provided the contents of a research paper.
Your task is to summarize the meeting notes as follows:

- Write a summary of the paper in 3-4 sentences.
- Write a list of key findings from the paper.
    - Write a list of supporting evidence for the key findings.
    - Write a list of refuting evidence for the key findings.
- Write a list of potential next steps or research directions.
""".strip()

question_prompt_template = """
Please provide a summary of the following text.
Write a concise summary of the following:
TEXT: {text}
SUMMARY:
""".strip()
question_prompt = PromptTemplate(
    template=question_prompt_template, input_variables=["text"]
)

refine_prompt_template = """
Write a concise summary of the following text delimited by triple backquotes.
Return your response in bullet points which covers the key points of the text.
```{text}```
BULLET POINT SUMMARY:
""".strip()
refine_prompt = PromptTemplate(
    template=refine_prompt_template, input_variables=["text"]
)

LLM_OPENAI = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-0125")
SUMMARIZE_CHAIN = AnalyzeDocumentChain(
    combine_docs_chain=load_summarize_chain(
        llm=LLM_OPENAI,
        chain_type="refine",
        question_prompt=question_prompt,
        refine_prompt=refine_prompt,
        return_intermediate_steps=False,
    ),
    text_splitter=RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=12288, chunk_overlap=1024
    ),
)


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
        message=topic, model="command-light", search_queries_only=True
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

    return "\n\n".join(
        f"{work_id}\n{summary}" for work_id, summary in zip(texts.keys(), summaries)
    )


async def summarize_text(text: str) -> str:
    """
    Summarize the contents of a research paper.

    Args:
        text (str): Contents of the paper

    Returns:
        str: Summary of the paper
    """

    return await SUMMARIZE_CHAIN.arun(text)
