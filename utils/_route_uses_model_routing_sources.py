
def _route_uses_model_routing_sources(route: str) -> bool:
    return _route_matches_any_marker(route=route, markers=_MODEL_ROUTING_ROUTE_MARKERS)

