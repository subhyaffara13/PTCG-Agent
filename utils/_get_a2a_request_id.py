
def _get_a2a_request_id(
    responses_so_far: List[Any], request_data: dict
) -> Optional[str]:
    """Get JSON-RPC request id from first A2A chunk or request body for in-stream error reporting."""
    for item in responses_so_far:
        if isinstance(item, dict) and "id" in item:
            return item.get("id")
        if isinstance(item, str):
            try:
                obj = json.loads(item.strip())
                if isinstance(obj, dict) and "id" in obj:
                    return obj.get("id")
            except (json.JSONDecodeError, TypeError):
                continue
    body = request_data.get("body") or request_data.get("data") or {}
    if isinstance(body, dict):
        return body.get("id")
    return None

