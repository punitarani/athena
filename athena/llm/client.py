"""athena/llm/client.py"""

import cohere
from groq import Groq
from openai import AsyncOpenAI

from athena import SECRETS

cohere = cohere.AsyncClient(api_key=SECRETS.COHERE_API_KEY)

groq = Groq(api_key=SECRETS.GROQ_API_KEY)

openai = AsyncOpenAI(api_key=SECRETS.OPENAI_API_KEY)
