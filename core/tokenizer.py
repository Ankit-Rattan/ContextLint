import tiktoken

def count_tokens(text: str, model_name: str = "gpt-4") -> int:
    """
    Counts the number of tokens in a text string using tiktoken.
    Defaults to gpt-4 encoding, which is highly accurate for most modern LLMs.
    """
    try:
        encoding = tiktoken.encoding_for_model(model_name)
    except KeyError:
        # Fallback if a specific model encoding isn't locally found
        encoding = tiktoken.get_encoding("cl100k_base")
        
    return len(encoding.encode(text))