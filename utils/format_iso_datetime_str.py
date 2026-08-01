
def format_iso_datetime_str(iso_datetime_str: Optional[str]) -> str:
    """Format an ISO format datetime string to human-readable date with minute resolution."""
    if not iso_datetime_str:
        return ""
    try:
        # Parse ISO format datetime string
        dt = datetime.fromisoformat(iso_datetime_str.replace("Z", "+00:00"))
        return dt.strftime("%Y-%m-%d %H:%M")
    except (TypeError, ValueError):
        return str(iso_datetime_str)

