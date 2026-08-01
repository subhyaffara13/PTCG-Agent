
def stripEscape(string: str) -> str:
    """Strip escape \\ characters"""
    return ESCAPE_CHAR.sub(r"\1", string)

