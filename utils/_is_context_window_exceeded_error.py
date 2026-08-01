
def _is_context_window_exceeded_error(exception) -> bool:
    """"""
    is_error = "ContextWindowExceededError" in str(type(exception))
    return is_error

