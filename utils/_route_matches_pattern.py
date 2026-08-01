
def _route_matches_pattern(route: str, pattern: str) -> bool:
    """
    Return True if the concrete route matches the pattern.
    Pattern segments like {param} match any single path segment.
    """
    route_parts = route.strip("/").split("/")
    pattern_parts = pattern.strip("/").split("/")
    if len(route_parts) != len(pattern_parts):
        return False
    for r, p in zip(route_parts, pattern_parts):
        if p.startswith("{") and p.endswith("}"):
            continue
        if r != p:
            return False
    return True

