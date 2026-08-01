
def get_access_path(key: str | Literal[0], parts: list[tuple[bool, str]]) -> str:
    """Given a list of format specifiers, returns
    the final access path (e.g. a.b.c[0][1]).
    """
    path = []
    for is_attribute, specifier in parts:
        if is_attribute:
            path.append(f".{specifier}")
        else:
            path.append(f"[{specifier!r}]")
    return str(key) + "".join(path)

