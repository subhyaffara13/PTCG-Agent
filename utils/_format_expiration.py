import time

def _format_expiration(expires_at: str | None) -> str:
    """Format an `expires_at` unix timestamp for display in `auth list`."""
    if not expires_at:
        return ""
    try:
        timestamp = int(expires_at)
    except ValueError:
        return ""
    date_str = datetime.fromtimestamp(timestamp).strftime("%Y-%m-%d")
    return f"{date_str} (expired)" if timestamp < time.time() else date_str

