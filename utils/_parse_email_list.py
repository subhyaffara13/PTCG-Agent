
def _parse_email_list(raw: Any) -> List[str]:
    """Parse emails from a list or comma-separated string."""
    if isinstance(raw, list):
        return [e.strip() for e in raw if isinstance(e, str) and e.strip()]
    elif isinstance(raw, str):
        return [e.strip() for e in raw.split(",") if e.strip()]
    return []

