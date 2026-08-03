from typing import Optional

def normalize_route_for_root_path(route: str) -> Optional[str]:
    """Strip SERVER_ROOT_PATH prefix. Returns de-prefixed route, or None if route is not under root path."""
    root_path = get_server_root_path()
    if root_path and root_path != "/":
        if route.startswith(root_path + "/"):
            return route[len(root_path) :]
        return None
    return route

