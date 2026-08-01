
def _strip_admin_only_fields_from_health_result(result: dict) -> dict:
    """
    Return a copy of the /health response with provider routing fields
    (``api_base``, ``api_version``) removed from each healthy/unhealthy
    endpoint entry. Used to hide those fields from non-admin callers while
    still showing them which deployments they own and whether each one is
    healthy. Proxy admins receive the unmodified result.
    """
    out = dict(result)
    drop = set(ADMIN_ONLY_HEALTH_DISPLAY_PARAMS)
    for key in ("healthy_endpoints", "unhealthy_endpoints"):
        eps = out.get(key)
        if isinstance(eps, list):
            out[key] = [
                (
                    {k: v for k, v in ep.items() if k not in drop}
                    if isinstance(ep, dict)
                    else ep
                )
                for ep in eps
            ]
    return out

