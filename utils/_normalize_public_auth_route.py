
def _normalize_public_auth_route(route: str) -> str:
    if route != "/" and route.endswith("/"):
        return route.rstrip("/")
    return route

