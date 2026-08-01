
def must_be_empty_body(method: str, code: int) -> bool:
    """Check if a request must return an empty body."""
    return (
        code in EMPTY_BODY_STATUS_CODES
        or method in EMPTY_BODY_METHODS
        or (200 <= code < 300 and method in hdrs.METH_CONNECT_ALL)
    )

