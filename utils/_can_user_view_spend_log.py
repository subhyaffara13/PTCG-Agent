
def _can_user_view_spend_log(user_api_key_dict: UserAPIKeyAuth) -> bool:
    """
    Check if the requesting user can view their own spend logs.
    """
    user_role = user_api_key_dict.user_role
    user_id = user_api_key_dict.user_id
    return (
        user_role
        in (
            LitellmUserRoles.INTERNAL_USER,
            LitellmUserRoles.INTERNAL_USER_VIEW_ONLY,
        )
        and user_id is not None
    )

