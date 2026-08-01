
def _byte_to_str_length(codec: str) -> int:
    """Return how many byte are usually(!) a character point."""
    if codec.startswith("utf-32"):
        return 4
    if codec.startswith("utf-16"):
        return 2

    return 1

