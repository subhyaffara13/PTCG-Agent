
def _find(tokens, token, value):
    '''Return the position of the last token with the same (token, value)
    pair supplied. The position is the one of the rightmost term.
    '''
    for index, token_values in enumerate(reversed(tokens)):
        if (token, value) == token_values[:2]:
            return len(tokens) - index - 1
    raise ValueError('(token, value) pair not found')


def _find(value: str, target: str, pos: int) -> int:
    """Find the *target* in *value* after *pos*.

    Returns the *value* length if *target* isn't found.
    """
    try:
        return value.index(target, pos)
    except ValueError:
        return len(value)

