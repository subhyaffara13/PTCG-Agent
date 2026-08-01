
def is_white_key(note):
    """True if note is represented by a white key"""

    key_pattern = [
        True,
        False,
        True,
        True,
        False,
        True,
        False,
        True,
        True,
        False,
        True,
        False,
    ]
    return key_pattern[(note - 21) % len(key_pattern)]

