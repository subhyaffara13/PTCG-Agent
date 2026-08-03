import re

def parse_pragma(pylint_pragma: str) -> Generator[PragmaRepresenter]:
    action: str | None = None
    messages: list[str] = []
    assignment_required = False
    previous_token = ""

    for mo in re.finditer(TOK_REGEX, pylint_pragma):
        kind = mo.lastgroup
        value = mo.group()

        if kind == "ASSIGN":
            if not assignment_required:
                if action:
                    # A keyword has been found previously but doesn't support assignment
                    raise UnRecognizedOptionError(
                        "The keyword doesn't support assignment", action
                    )
                if previous_token:
                    # Something found previously but not a known keyword
                    raise UnRecognizedOptionError(
                        "The keyword is unknown", previous_token
                    )
                # Nothing at all detected before this assignment
                raise InvalidPragmaError("Missing keyword before assignment", "")
            assignment_required = False
        elif assignment_required:
            raise InvalidPragmaError(
                "The = sign is missing after the keyword", action or ""
            )
        elif kind == "KEYWORD":
            if action:
                yield emit_pragma_representer(action, messages)
            action = value
            messages = []
            assignment_required = action in MESSAGE_KEYWORDS
        elif kind in {"MESSAGE_STRING", "MESSAGE_NUMBER"}:
            messages.append(value)
            assignment_required = False
        else:
            raise RuntimeError("Token not recognized")

        previous_token = value

    if action:
        yield emit_pragma_representer(action, messages)
    else:
        raise UnRecognizedOptionError("The keyword is unknown", previous_token)

