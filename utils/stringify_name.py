
def stringify_name(n: AST) -> str | None:
    if isinstance(n, Name):
        return n.id
    elif isinstance(n, Attribute):
        sv = stringify_name(n.value)
        if sv is not None:
            return f"{sv}.{n.attr}"
    return None  # Can't do it.

