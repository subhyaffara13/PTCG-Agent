
def _is_unexpected_keyword_argument_type_error(exc: BaseException) -> bool:
    """True when ``exc`` is a TypeError from passing a kwarg the callee does not accept."""
    return isinstance(exc, TypeError) and (
        "unexpected keyword argument" in str(exc).lower()
    )

