
def _detect_line_ending(content: str) -> Literal["\r", "\n", "\r\n", None]:  # noqa: F722
    """Detect the line ending of a string. Used by RepoCard to avoid making huge diff on newlines.

    Uses same implementation as in Hub server, keep it in sync.

    Returns:
        str: The detected line ending of the string.
    """
    cr = content.count("\r")
    lf = content.count("\n")
    crlf = content.count("\r\n")
    if cr + lf == 0:
        return None
    if crlf == cr and crlf == lf:
        return "\r\n"
    if cr > lf:
        return "\r"
    else:
        return "\n"

