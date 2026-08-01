
def _add_wildcard_to_directories(pattern: str) -> str:
    if pattern.endswith("/"):
        return pattern + "*"
    return pattern

