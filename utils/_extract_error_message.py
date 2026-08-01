
def _extract_error_message(e: Exception) -> str:
    """Extract a human-readable error message from a guardrail exception."""
    if isinstance(e, ModifyResponseException):
        return str(e)
    if HTTPException is not None and isinstance(e, HTTPException):
        detail = getattr(e, "detail", None)
        if detail:
            return str(detail)
    return str(e)

