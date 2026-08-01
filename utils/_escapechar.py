
def _escapechar(c: str) -> str:
    """Helper function for tagToIdentifier()"""
    import re

    if re.match("[a-z0-9]", c):
        return "_" + c
    elif re.match("[A-Z]", c):
        return c + "_"
    else:
        return hex(byteord(c))[2:]

