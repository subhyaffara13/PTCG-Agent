
def detect_first_expected_role(
    messages: List[AllMessageValues],
) -> Optional[Literal["user", "assistant"]]:
    """
    Detect the first expected role based on the message sequence.

    Rules:
    1. If messages list is empty, assume 'user' starts
    2. If first message is from assistant, expect 'user' next
    3. If first message is from user, expect 'assistant' next
    4. If first message is system, look at the next non-system message

    Returns:
        str: Either 'user' or 'assistant'
        None: If no 'user' or 'assistant' messages provided
    """
    if not messages:
        return "user"

    for message in messages:
        if message["role"] == "system":
            continue
        return "user" if message["role"] == "assistant" else "assistant"

    return None

