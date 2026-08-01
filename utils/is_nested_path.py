
def is_nested_path(path: str) -> bool:
    """
    Check if path requires nested handling.

    Returns True if path contains '.' or '[' (array notation).
    """
    return "." in path or "[" in path

