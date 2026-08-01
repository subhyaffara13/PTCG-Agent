
def _parse_metadata(raw_metadata: object) -> dict:
    """Parse metadata that may be a dict, JSON string, or None."""
    if raw_metadata is None:
        return {}
    if isinstance(raw_metadata, str):
        try:
            return json.loads(raw_metadata)
        except (json.JSONDecodeError, TypeError):
            return {}
    return raw_metadata if isinstance(raw_metadata, dict) else {}

