
def _key_metadata(
    api_key_metadata: Dict[str, Dict[str, Any]], api_key: str
) -> KeyMetadata:
    meta = api_key_metadata.get(api_key, {})
    return KeyMetadata(key_alias=meta.get("key_alias"), team_id=meta.get("team_id"))

