
def currently_sharing() -> bool:
    """Check if we are currently sharing a cache -- thread specific."""
    return threading.get_ident() in _SHARING_STACK

