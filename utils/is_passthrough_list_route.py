
def is_passthrough_list_route(provider: str, method: str, route: str) -> bool:
    """Return True when this is a GET list route whose results should be served
    from the DB (user-scoped) rather than forwarded upstream."""
    if method != "GET":
        return False
    from litellm.proxy.auth.auth_utils import normalize_request_route

    canonical = normalize_request_route(_canonical_path(route))
    return (provider, canonical) in _LIST_ROUTE_TABLE

