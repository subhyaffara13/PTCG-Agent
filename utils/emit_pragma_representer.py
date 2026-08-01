
def emit_pragma_representer(action: str, messages: list[str]) -> PragmaRepresenter:
    if not messages and action in MESSAGE_KEYWORDS:
        raise InvalidPragmaError(
            "The keyword is not followed by message identifier", action
        )
    return PragmaRepresenter(action, messages)

