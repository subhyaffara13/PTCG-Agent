from typing import Optional

def get_request_route_template(request: Request) -> Optional[str]:
    """
    Return the low-cardinality route template, e.g.
    ``/v1/threads/{thread_id}/runs`` (vs. the literal path from
    ``get_request_route``). FastAPI sets ``scope["route"]`` before endpoint
    dependencies run. Returns None if unavailable (unmatched path, Mount).
    """
    try:
        scope = request.scope
        if not isinstance(scope, dict):
            return None
        route = scope.get("route")
        template = getattr(route, "path", None)
        return template if isinstance(template, str) and template else None
    except Exception as e:
        verbose_proxy_logger.debug(f"error on get_request_route_template: {str(e)}")
        return None

