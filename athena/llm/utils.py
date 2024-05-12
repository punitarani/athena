"""athena/llm/utils.py"""

import tiktoken

tokenizer = tiktoken.get_encoding("cl100k_base")


def get_token_count(text: str) -> int:
    """Get the number of tokens in the text."""
    return len(tokenizer.encode(text))
