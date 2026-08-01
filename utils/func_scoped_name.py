
def func_scoped_name(name: str, line: int) -> str:
    """Mangled name to use when storing function-scoped symbols in global symbol tables."""
    return f"{name}@{line}"

