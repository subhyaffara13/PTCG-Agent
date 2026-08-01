
def new_chat_history(system_prompt: str | None = None) -> list[dict]:
    """Returns a new chat conversation."""
    return [{"role": "system", "content": system_prompt}] if system_prompt else []

