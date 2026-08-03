from typing import Optional

def _write_health_state_to_router_cache(
    healthy_endpoints: list,
    unhealthy_endpoints: list,
    exceptions_by_model_id: Optional[dict] = None,
) -> None:
    """
    Write deployment health states to the router's health state cache
    for health-check-driven routing. No-op if the feature is disabled.
    """
    from litellm.proxy.health_check import build_deployment_health_states
    from litellm.router_utils.cooldown_handlers import _set_cooldown_deployments
    from litellm.router_utils.router_callbacks.track_deployment_metrics import (
        increment_deployment_failures_for_current_minute,
    )

    _exceptions: dict = exceptions_by_model_id or {}

    try:
        if llm_router is None or not llm_router.enable_health_check_routing:
            return

        # When health_check_ignore_transient_errors is set, treat 429/408
        # endpoints as healthy so they are not filtered from routing.
        _effective_unhealthy = unhealthy_endpoints
        if llm_router.health_check_ignore_transient_errors:
            _effective_unhealthy = [
                ep
                for ep in unhealthy_endpoints
                if _get_endpoint_exception_status(ep, _exceptions) not in (429, 408)
            ]

        states = build_deployment_health_states(
            healthy_endpoints=healthy_endpoints,
            unhealthy_endpoints=_effective_unhealthy,
        )
        if states:
            llm_router.health_state_cache.set_deployment_health_states(states)
            verbose_proxy_logger.debug(
                "health_check_routing_state_updated healthy=%d unhealthy=%d",
                sum(1 for s in states.values() if s.get("is_healthy")),
                sum(1 for s in states.values() if not s.get("is_healthy")),
            )

        for endpoint in unhealthy_endpoints:
            model_id = endpoint.get("model_id")
            if not model_id:
                continue

            original_exception = _exceptions.get(model_id)
            if original_exception is None:
                continue

            exception_status = getattr(original_exception, "status_code", 500)

            if (
                llm_router.health_check_ignore_transient_errors
                and exception_status
                in (
                    429,
                    408,
                )
            ):
                continue

            increment_deployment_failures_for_current_minute(
                litellm_router_instance=llm_router,
                deployment_id=model_id,
            )

            _set_cooldown_deployments(
                litellm_router_instance=llm_router,
                original_exception=original_exception,
                exception_status=exception_status,
                deployment=model_id,
                time_to_cooldown=llm_router.cooldown_time,
            )

    except Exception as e:
        verbose_proxy_logger.warning(
            "Failed to write health state to router cache: %s", str(e)
        )

