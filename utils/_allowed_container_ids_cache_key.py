
def _allowed_container_ids_cache_key(owner_scopes: List[str]) -> str:
    """JSON-encode the sorted scope list — using a separator like ``|``
    would collide for any tenant whose user_id / team_id / org_id /
    api_key happens to contain the separator. JSON quoting escapes
    every separator that matters."""
    return json.dumps(sorted(owner_scopes))

