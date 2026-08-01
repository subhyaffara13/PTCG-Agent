
def _format_trimmed(format: str, msg: str, available_width: int) -> str | None:
    """Format msg into format, ellipsizing it if doesn't fit in available_width.

    Returns None if even the ellipsis can't fit.
    """
    # Only use the first line.
    i = msg.find("\n")
    if i != -1:
        msg = msg[:i]

    ellipsis = "..."
    format_width = wcswidth(format.format(""))
    if format_width + len(ellipsis) > available_width:
        return None

    if format_width + wcswidth(msg) > available_width:
        available_width -= len(ellipsis)
        msg = msg[:available_width]
        while format_width + wcswidth(msg) > available_width:
            msg = msg[:-1]
        msg += ellipsis

    return format.format(msg)

