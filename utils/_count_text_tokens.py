
def _count_text_tokens(model: str, text: Any) -> int:
    if text is None:
        return 0

    token_count = 0
    stack = [text]
    while stack:
        item = stack.pop()
        if item is None:
            continue
        if isinstance(item, list):
            stack.extend(item)
            continue
        if isinstance(item, dict):
            token_count += litellm.token_counter(model=model, text=json.dumps(item))
            continue
        token_count += litellm.token_counter(model=model, text=str(item))
    return token_count

