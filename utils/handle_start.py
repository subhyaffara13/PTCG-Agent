
def handle_start(char: str, pos: int, tokens: TokenState) -> State:
    if char == "{":
        return State.SCANNING
    raise ParseError("Attributes must start with '{'", pos)

