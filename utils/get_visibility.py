
def get_visibility(name: str) -> str:
    """Return the visibility from a name: public, protected, private or special."""
    if SPECIAL.match(name):
        visibility = "special"
    elif PRIVATE.match(name):
        visibility = "private"
    elif PROTECTED.match(name):
        visibility = "protected"

    else:
        visibility = "public"
    return visibility

