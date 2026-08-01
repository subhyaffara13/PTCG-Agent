
def _is_allowed_to_make_key_request(
    user_api_key_dict: UserAPIKeyAuth,
    user_id: Optional[str],
    team_id: Optional[str],
) -> bool:
    """
    Assert user only creates/updates keys for themselves

    Relevant issue: https://github.com/BerriAI/litellm/issues/7336
    """
    ## BASE CASE - PROXY ADMIN
    if (
        user_api_key_dict.user_role is not None
        and user_api_key_dict.user_role == LitellmUserRoles.PROXY_ADMIN.value
    ):
        return True

    if user_id is not None:
        assert (
            user_id == user_api_key_dict.user_id
        ), "User can only create keys for themselves. Got user_id={}, Your ID={}".format(
            user_id, user_api_key_dict.user_id
        )

    if team_id is not None:
        if (
            user_api_key_dict.team_id is not None
            and user_api_key_dict.team_id == UI_TEAM_ID
        ):
            return True  # handle https://github.com/BerriAI/litellm/issues/7482

    return True

