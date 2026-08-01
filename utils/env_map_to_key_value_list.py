
def env_map_to_key_value_list(env_map: dict[str, str | None]) -> list[dict[str, str]] | None:
    """Convert an env/secrets dict to the ``[{"key": ..., "value": ...}]`` format used by the Hub API."""
    if not env_map:
        return None
    return [{"key": k, "value": v or ""} for k, v in env_map.items()]

