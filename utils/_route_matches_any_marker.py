from typing import Tuple

def _route_matches_any_marker(route: str, markers: Tuple[str, ...]) -> bool:
    normalized_route = route.lower()
    return any(marker in normalized_route for marker in markers)

