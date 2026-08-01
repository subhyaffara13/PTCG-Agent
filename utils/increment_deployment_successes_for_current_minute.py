
def increment_deployment_successes_for_current_minute(
    litellm_router_instance: LitellmRouter,
    deployment_id: str,
) -> str:
    """
    In-Memory: Increments the number of successes for the current minute for a deployment_id
    """
    key = f"{deployment_id}:successes"
    litellm_router_instance.cache.increment_cache(
        local_only=True,
        key=key,
        value=1,
        ttl=60,
    )
    return key

