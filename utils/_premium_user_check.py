
def _premium_user_check(feature: Optional[str] = None):
    """
    Raises an HTTPException if the user is not a premium user
    """
    from litellm.proxy.proxy_server import premium_user

    if feature:
        detail_msg = f"This feature is only available for LiteLLM Enterprise users: {feature}. {CommonProxyErrors.not_premium_user.value}"
    else:
        detail_msg = f"This feature is only available for LiteLLM Enterprise users. {CommonProxyErrors.not_premium_user.value}"

    if not premium_user:
        raise HTTPException(
            status_code=403,
            detail={"error": detail_msg},
        )

