
def _managed_id_matches_provider(unified_id: str, provider: str) -> bool:
    payload = decode(unified_id)
    return payload is not None and payload.provider == provider

