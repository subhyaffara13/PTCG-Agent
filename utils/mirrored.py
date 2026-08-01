
def mirrored(code):
    """If code (unicode codepoint) has a mirrored version returns it, otherwise None."""
    return Mirrored.MIRRORED.get(code)

