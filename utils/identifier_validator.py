
def identifierValidator(value: Any) -> bool:
    """
    Version 3+.

    >>> identifierValidator("a")
    True
    >>> identifierValidator("")
    False
    >>> identifierValidator("a" * 101)
    False
    """
    validCharactersMin = 0x20
    validCharactersMax = 0x7E
    if not isinstance(value, str):
        return False
    if not value:
        return False
    if len(value) > 100:
        return False
    for c in value:
        i = ord(c)
        if i < validCharactersMin or i > validCharactersMax:
            return False
    return True

