
def handle_scanning_comment(char: str, pos: int, tokens: TokenState) -> State:
    if char == "%":
        return State.SCANNING

    return State.SCANNING_COMMENT

