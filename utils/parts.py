
def parts(s: str) -> set[str]:
    parts = s.split(sep)
    return {sep.join(parts[: i + 1]) or sep for i in range(len(parts))}

