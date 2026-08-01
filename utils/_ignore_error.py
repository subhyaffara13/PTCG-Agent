
def _ignore_error(exception: Exception) -> bool:
    return (
        getattr(exception, "errno", None) in _IGNORED_ERRORS
        or getattr(exception, "winerror", None) in _IGNORED_WINERRORS
    )

