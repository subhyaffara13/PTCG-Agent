
def format_session_duration(seconds: float) -> str:
    """Format the given seconds in a human readable manner to show in the final summary."""
    if seconds < 60:
        return f"{seconds:.2f}s"
    else:
        dt = datetime.timedelta(seconds=int(seconds))
        return f"{seconds:.2f}s ({dt})"

