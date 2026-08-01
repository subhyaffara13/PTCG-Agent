
def format_date(dt: datetime | None, human_readable: bool = False) -> str:
    """Format a datetime to a readable date string."""
    if dt is None:
        return ""
    if human_readable:
        return dt.strftime("%b %d %H:%M")
    return dt.strftime("%Y-%m-%d %H:%M:%S")

