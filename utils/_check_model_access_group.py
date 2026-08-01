
def _check_model_access_group(
    models: Optional[List[str]], llm_router: Optional[Router], premium_user: bool
) -> Literal[True]:
    """
    if is_model_access_group is True + is_wildcard_route is True, check if user is a premium user

    Return True if user is a premium user, False otherwise
    """
    if models is None or llm_router is None:
        return True

    for model in models:
        if llm_router._is_model_access_group_for_wildcard_route(
            model_access_group=model
        ):
            if not premium_user:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail={
                        "error": "Setting a model access group on a wildcard model is only available for LiteLLM Enterprise users.{}".format(
                            CommonProxyErrors.not_premium_user.value
                        )
                    },
                )

    return True

