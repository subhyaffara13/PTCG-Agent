
def _count_entry_tokens(
    entry: dict,
    model_name: Optional[str] = None,
) -> int:
    """Token-count a single batch input entry's body (chat / text / embedding)."""
    body = entry.get("body", {}) or {}
    model = body.get("model", model_name or "")

    messages = body.get("messages")
    if messages:
        return token_counter(model=model, messages=messages)

    prompt = body.get("prompt")
    if prompt:
        return _count_prompt_or_input_tokens(model=model, value=prompt)

    input_data = body.get("input")
    if input_data:
        return _count_prompt_or_input_tokens(model=model, value=input_data)

    return 0

