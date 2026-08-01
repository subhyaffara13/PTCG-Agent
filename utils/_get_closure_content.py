
def _get_closure_content(content: types.CellType) -> object:
    if callable(content) and hasattr(content, "__code__"):
        return content.__code__
    return None

