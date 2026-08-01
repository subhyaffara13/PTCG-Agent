
def _is_above_128k(tokens: float) -> bool:
    if tokens > 128000:
        return True
    return False

