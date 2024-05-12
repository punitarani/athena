"""athena/llm/skills/summary.py"""

from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.chains.llm import LLMChain
from langchain.prompts import PromptTemplate

from langchain_groq import ChatGroq

prompt_template = """Write a concise summary of the following:
"{text}"
CONCISE SUMMARY:"""
prompt = PromptTemplate.from_template(prompt_template)
llm = ChatGroq(temperature=0, model_name="llama-8b-8192")
llm_chain = LLMChain(llm=llm, prompt=prompt)
stuff_chain = StuffDocumentsChain(llm_chain=llm_chain, document_variable_name="text")


async def summarize_text(text: str) -> str:
    """
    Summarize the contents of a research paper.

    Args:
        text (str): Contents of the paper

    Returns:
        str: Summary of the paper
    """

    return await stuff_chain.run(text=text)
