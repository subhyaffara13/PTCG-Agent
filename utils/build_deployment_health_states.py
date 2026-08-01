
def build_deployment_health_states(
    healthy_endpoints: list,
    unhealthy_endpoints: list,
) -> dict:
    """
    Build a dict mapping deployment_id -> DeploymentHealthStateValue from
    health check endpoint results.

    Each endpoint dict includes a 'model_id' field (added by _perform_health_check)
    that maps back to the deployment's model_info.id.

    Used by the background health check loop to feed health state into
    the router's DeploymentHealthCache for health-check-driven routing.
    """
    now = time.time()
    states: dict = {}

    for ep in healthy_endpoints:
        model_id = ep.get("model_id")
        if model_id:
            states[model_id] = {
                "is_healthy": True,
                "timestamp": now,
                "reason": "",
            }

    for ep in unhealthy_endpoints:
        model_id = ep.get("model_id")
        if model_id:
            states[model_id] = {
                "is_healthy": False,
                "timestamp": now,
                "reason": "background_health_check_failed",
            }

    return states

