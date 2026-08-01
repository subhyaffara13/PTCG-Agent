
def _is_converse_endpoint(endpoint: str) -> bool:
    parts = endpoint.rstrip("/").split("/")
    return bool(parts) and parts[-1] in _CONVERSE_ACTIONS

