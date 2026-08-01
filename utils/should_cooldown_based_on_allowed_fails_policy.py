
def should_cooldown_based_on_allowed_fails_policy(
    litellm_router_instance: LitellmRouter,
    deployment: str,
    original_exception: Any,
) -> bool:
    """
    Check if fails are within the allowed limit and update the number of fails.

    Returns:
    - True if fails exceed the allowed limit (should cooldown)
    - False if fails are within the allowed limit (should not cooldown)
    """
    allowed_fails = (
        litellm_router_instance.get_allowed_fails_from_policy(
            exception=original_exception,
        )
        or litellm_router_instance.allowed_fails
    )
    cooldown_time = (
        litellm_router_instance.cooldown_time or DEFAULT_COOLDOWN_TIME_SECONDS
    )

    current_fails = litellm_router_instance.failed_calls.get_cache(key=deployment) or 0
    updated_fails = current_fails + 1

    if updated_fails > allowed_fails:
        return True
    else:
        litellm_router_instance.failed_calls.set_cache(
            key=deployment, value=updated_fails, ttl=cooldown_time
        )

    return False

