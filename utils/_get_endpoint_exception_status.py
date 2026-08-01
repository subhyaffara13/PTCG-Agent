
def _get_endpoint_exception_status(endpoint: dict, exceptions: dict) -> int:
    """Return the HTTP status code for an unhealthy endpoint.

    Prefers the live exception object in `exceptions` (direct health check path).
    Falls back to the `exception_status` integer stored on the endpoint dict
    (shared-cache path, where exception objects are not available).
    """
    model_id = endpoint.get("model_id")
    exc = exceptions.get(model_id) if model_id else None
    if exc is not None:
        return getattr(exc, "status_code", 500)
    return endpoint.get("exception_status", 500)

