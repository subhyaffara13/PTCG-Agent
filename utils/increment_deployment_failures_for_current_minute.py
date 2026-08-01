
def increment_deployment_failures_for_current_minute(
    litellm_router_instance: LitellmRouter,
    deployment_id: str,
):
    """
    In-Memory: Increments the number of failures for the current minute for a deployment_id
    """
    key = f"{deployment_id}:fails"
    litellm_router_instance.cache.increment_cache(
        local_only=True,
        key=key,
        value=1,
        ttl=60,
    )

