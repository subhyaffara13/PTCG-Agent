
def format_timestamp(timestamp: Optional[int]) -> str:
    """Format a Unix timestamp (integer) to human-readable date with minute resolution."""
    if timestamp is None:
        return ""
    try:
        dt = datetime.fromtimestamp(timestamp)
        return dt.strftime("%Y-%m-%d %H:%M")
    except (TypeError, ValueError):
        return str(timestamp)

