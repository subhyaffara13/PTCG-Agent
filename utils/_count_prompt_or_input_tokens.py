
def _count_prompt_or_input_tokens(model: str, value: Any) -> int:
    """Token-count a ``prompt`` / ``input`` field that the OpenAI batch
    schema allows in four shapes:

    - ``str``: a single text prompt.
    - ``list[str]``: multiple text prompts.
    - ``list[int]``: a pre-tokenized prompt (each int counts as 1 token).
    - ``list[list[int]]``: multiple pre-tokenized prompts.

    Pre-fix only the string shapes were counted, so a caller could send
    a large ``list[list[int]]`` payload and slip past TPM rate limits
    with a recorded cost of zero tokens.
    """
    if isinstance(value, str):
        return token_counter(model=model, text=value)
    if isinstance(value, list):
        total = 0
        for chunk in value:
            if isinstance(chunk, str):
                total += token_counter(model=model, text=chunk)
            elif isinstance(chunk, int):
                # Single pre-tokenized prompt at the top level: each
                # int counts as one token.
                total += 1
            elif isinstance(chunk, list):
                # Nested pre-tokenized prompt: every int contributes a
                # token. Mixed string/int items still count.
                total += sum(1 if isinstance(t, int) else 0 for t in chunk)
                total += sum(
                    token_counter(model=model, text=t)
                    for t in chunk
                    if isinstance(t, str)
                )
        return total
    return 0

