
def get_first_not_none(a: Any, b: Any) -> Any:
    """Return the first argument if it is not `None`, otherwise return the second argument."""
    return a if a is not None else b

