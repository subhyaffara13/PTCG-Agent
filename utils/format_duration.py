
def format_duration(secs: int | None) -> str:
    """Format a duration in seconds as a short human-readable string (e.g. `"1m 32s"`, `"2h 15m"`, `"45s"`).

    Returns `"--"` when `secs` is `None` so it can be used directly as a CLI table cell.
    """
    if secs is None:
        return "--"
    secs = int(secs)
    if secs < 60:
        return f"{secs}s"
    if secs < 3600:
        return f"{secs // 60}m {secs % 60}s"
    return f"{secs // 3600}h {(secs % 3600) // 60}m"

