import json

def _filtered_team_metadata_json(
    metadata: Mapping[str, object] | None,
    allowed_keys: tuple[str, ...],
) -> str | None:
    """JSON-serialize only the allowlisted sub-keys of a team's metadata.

    Returns ``None`` when nothing is allowlisted or no allowlisted key is
    present, so the empty case is dropped rather than promoting ``"{}"``. Keys
    are sorted for a stable, diff-friendly value.
    """
    if not isinstance(metadata, Mapping) or not allowed_keys:
        return None
    filtered = {key: metadata[key] for key in allowed_keys if key in metadata}
    if not filtered:
        return None
    return json.dumps(filtered, default=str, sort_keys=True)

