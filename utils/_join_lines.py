
def _join_lines(lines):
    """join lines that have been written by splitlines()

    Has logic to protect against `splitlines()`, which
    should have been `splitlines(True)`
    """
    if lines and lines[0].endswith(("\n", "\r")):
        # created by splitlines(True)
        return "".join(lines)
    # created by splitlines()
    return "\n".join(lines)

