
def _normalize_team_metadata_keys(value: Any) -> List[str]:
    """Coerce a team-metadata allowlist from a list or comma-separated string.

    config.yaml passes a YAML list; an env var passes a comma-separated string.
    Both collapse to a list of stripped, non-empty keys.
    """
    if value is None:
        return []
    if isinstance(value, str):
        return [item.strip() for item in value.split(",") if item.strip()]
    return [str(item).strip() for item in value if str(item).strip()]

