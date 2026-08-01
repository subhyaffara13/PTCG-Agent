
def handle_scanning_escaped(char: str, pos: int, tokens: TokenState) -> State:
    return State.SCANNING_QUOTED_VALUE

