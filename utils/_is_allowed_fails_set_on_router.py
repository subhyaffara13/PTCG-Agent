
def _is_allowed_fails_set_on_router(
    litellm_router_instance: LitellmRouter,
) -> bool:
    """
    Check if Router.allowed_fails is set or is Non-default Value

    Returns:
    - True if Router.allowed_fails is set or is Non-default Value
    - False if Router.allowed_fails is None or is Default Value
    """
    if litellm_router_instance.allowed_fails is None:
        return False
    if litellm_router_instance.allowed_fails != litellm.allowed_fails:
        return True
    return False

