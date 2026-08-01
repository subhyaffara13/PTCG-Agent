
def _is_admin_view_safe(user_api_key_dict: UserAPIKeyAuth) -> bool:
    """
    Safely determine if the current user has admin view permissions.
    Defaults to False on any exception.
    """
    try:
        user_role = getattr(user_api_key_dict, "user_role", None)
        if user_role is None:
            return False
        return user_role in (
            LitellmUserRoles.PROXY_ADMIN,
            LitellmUserRoles.PROXY_ADMIN_VIEW_ONLY,
        )
    except Exception:
        return False

