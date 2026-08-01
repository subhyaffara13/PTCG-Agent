
def _parse_expires_at(fields: dict[str, str]) -> int | None:
    """Parse the `expires_at` field of a stored-tokens section, `None` if missing or corrupt."""
    try:
        return int(fields["expires_at"])
    except (KeyError, ValueError):
        return None

