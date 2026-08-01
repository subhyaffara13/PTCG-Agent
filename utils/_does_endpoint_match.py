
def _does_endpoint_match(endpoint_path: str, request_path: str) -> bool:
    if endpoint_path in request_path:
        return True
    if "{" in endpoint_path:
        prefix = endpoint_path.split("{", 1)[0]
        if prefix and prefix in request_path:
            return True
    return False

