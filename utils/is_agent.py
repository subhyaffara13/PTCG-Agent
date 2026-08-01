
def is_agent() -> bool:
    """Return `True` if the process is being invoked by an AI coding agent."""
    return detect_agent() is not None

