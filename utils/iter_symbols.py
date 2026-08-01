
def iter_symbols(code: CodeType) -> Iterator[str]:
    """Yield names and strings used by `code` and its nested code objects"""
    yield from code.co_names
    for const in code.co_consts:
        if isinstance(const, str):
            yield const
        elif isinstance(const, CodeType):
            yield from iter_symbols(const)

