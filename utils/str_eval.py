
def str_eval(token: str) -> str:
    """Mostly replicate `ast.literal_eval(token)` manually to avoid any performance hit.

    This supports f-strings, contrary to `ast.literal_eval`.
    We have to support all string literal notations:
    https://docs.python.org/3/reference/lexical_analysis.html#string-and-bytes-literals
    """
    if token[0:2].lower() in {"fr", "rf"}:
        token = token[2:]
    elif token[0].lower() in {"r", "u", "f"}:
        token = token[1:]
    if token[0:3] in {'"""', "'''"}:
        return token[3:-3]
    return token[1:-1]

