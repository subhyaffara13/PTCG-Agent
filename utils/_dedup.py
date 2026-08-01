
def _dedup(a: str, b: str) -> tuple[str] | tuple[str, str]:
    return (a, b) if a != b else (a,)

