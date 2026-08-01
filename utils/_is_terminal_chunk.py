
def _is_terminal_chunk(chunk: OpenAIChatCompletionChunk) -> bool:
    """OpenAI-shaped chunk is terminal if any choice has a non-None finish_reason."""
    try:
        for ch in chunk.choices or []:
            if ch.finish_reason is not None:
                return True
    except Exception:
        pass
    return False

