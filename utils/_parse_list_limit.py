
def _parse_list_limit(query_params: Optional[Dict[str, Any]]) -> Tuple[int, int]:
    params = query_params or {}
    try:
        raw_limit = int(params.get("limit", 20))
    except (TypeError, ValueError):
        raw_limit = 20
    # Fetch one extra to cheaply detect has_more.
    return raw_limit, min(raw_limit, 100) + 1

