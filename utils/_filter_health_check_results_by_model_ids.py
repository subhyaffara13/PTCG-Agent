
def _filter_health_check_results_by_model_ids(
    results: dict, allowed_model_ids: set
) -> dict:
    """
    Restrict a cached background health-check result dict to endpoints whose
    model_id is in ``allowed_model_ids``.

    Endpoints without a model_id (e.g. CLI-model entries that predate the
    model_id wiring) are dropped conservatively — we cannot prove they belong
    to the caller, so they are excluded rather than leaked.

    Each retained endpoint is shallow-copied before being returned, so any
    downstream transform (e.g. _strip_admin_only_fields_from_health_result)
    cannot accidentally mutate the shared ``health_check_results`` cache.
    """
    healthy = [
        dict(ep)
        for ep in (results.get("healthy_endpoints") or [])
        if ep.get("model_id") in allowed_model_ids
    ]
    unhealthy = [
        dict(ep)
        for ep in (results.get("unhealthy_endpoints") or [])
        if ep.get("model_id") in allowed_model_ids
    ]
    return {
        "healthy_endpoints": healthy,
        "unhealthy_endpoints": unhealthy,
        "healthy_count": len(healthy),
        "unhealthy_count": len(unhealthy),
    }

