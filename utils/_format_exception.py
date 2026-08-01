
def _format_exception(e: Exception) -> str:
    """Format the full traceback as Python would show it."""
    return "\n".join(traceback.format_exception(type(e), e, e.__traceback__))

