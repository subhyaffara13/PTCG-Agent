
def format_size(bytes: float) -> str:
    if bytes > 1000 * 1000:
        return f"{bytes / 1000.0 / 1000:.1f} MB"
    elif bytes > 10 * 1000:
        return f"{int(bytes / 1000)} kB"
    elif bytes > 1000:
        return f"{bytes / 1000.0:.1f} kB"
    else:
        return f"{int(bytes)} bytes"


def format_size(size: int | float, human_readable: bool = False) -> str:
    """Format a size in bytes."""
    if not human_readable:
        return str(size)

    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size < 1000:
            if unit == "B":
                return f"{size} {unit}"
            return f"{size:.1f} {unit}"
        size /= 1000
    return f"{size:.1f} PB"

