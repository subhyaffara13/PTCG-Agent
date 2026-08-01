
def match_extensions(filename: str, extensions: Iterable) -> bool:
    """Helper method to see if filename ends with certain extension"""
    return any(filename.endswith(e) for e in extensions)

