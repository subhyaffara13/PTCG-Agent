
def get_deployment_failures_for_current_minute(
    litellm_router_instance: LitellmRouter,
    deployment_id: str,
) -> int:
    """
    Returns the number of fails for the current minute for a deployment_id

    Returns 0 if no value found
    """
    key = f"{deployment_id}:fails"
    return (
        litellm_router_instance.cache.get_cache(
            local_only=True,
            key=key,
        )
        or 0
    )

