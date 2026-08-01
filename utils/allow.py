
def allow() -> Dict[str, Any]:
    """
    Allow the request/response to proceed unchanged.

    Returns:
        Dict indicating the request should be allowed
    """
    return {"action": "allow"}

