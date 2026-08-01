
def handle_scanning_id(char: str, pos: int, tokens: TokenState) -> State:
    if not REGEX_SPACE_PUNCTUATION.fullmatch(char):
        return State.SCANNING_ID

    if char == "}":
        if (pos - 1) > tokens.start:
            tokens.append(tokens.start + 1, pos, "id")
        return State.DONE

    if REGEX_SPACE.fullmatch(char):
        if (pos - 1) > tokens.start:
            tokens.append(tokens.start + 1, pos, "id")
        return State.SCANNING

    raise ParseError(f"Unexpected character whilst scanning id: {char}", pos)

