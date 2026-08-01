
def _get_tags_from_metadata(metadata: object, json_metadata: object = None) -> list:
    """Extract tags list from a metadata field (or metadata_json fallback)."""
    raw = json_metadata if json_metadata is not None else metadata
    parsed = _parse_metadata(raw)
    return parsed.get("tags", []) or []

