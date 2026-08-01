
def get_funcname(filename: str, lineno: int) -> str | None:
    if filename not in cache:
        _add_file(filename)
    return cache[filename].get(lineno, None)

