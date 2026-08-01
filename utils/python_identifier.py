
def python_identifier(value: str) -> bool:
    """Can be used as identifier in Python.
    (Validation uses :obj:`str.isidentifier`).
    """
    return value.isidentifier()

