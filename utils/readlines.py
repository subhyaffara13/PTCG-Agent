
def readlines(filename):
    """Read the source code."""
    try:
        with tokenize.open(filename) as f:
            return f.readlines()
    except (LookupError, SyntaxError, UnicodeError):
        # Fall back if file encoding is improperly declared
        with open(filename, encoding='latin-1') as f:
            return f.readlines()


def readlines(path):
    with open(path, "r", encoding="ascii") as f:
        data = f.read()
    return data.splitlines()

