
def plugin(version: str) -> type[Plugin]:
    """`version` is the mypy version string.

    We might want to use this to print a warning if the mypy version being used is
    newer, or especially older, than we expect (or need).

    Args:
        version: The mypy version string.

    Return:
        The Pydantic mypy plugin type.
    """
    return PydanticPlugin


def plugin(version: str) -> 'TypingType[Plugin]':
    """
    `version` is the mypy version string

    We might want to use this to print a warning if the mypy version being used is
    newer, or especially older, than we expect (or need).
    """
    return PydanticPlugin


def plugin(version: str) -> type[ProperTypePlugin]:
    return ProperTypePlugin

