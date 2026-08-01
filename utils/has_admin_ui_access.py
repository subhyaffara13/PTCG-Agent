
def has_admin_ui_access(user_role: str) -> bool:
    """
    Check if the user has admin access to the UI.

    Returns:
        bool: True if user is 'proxy_admin' or 'proxy_admin_view_only', False otherwise.
    """

    if (
        user_role != LitellmUserRoles.PROXY_ADMIN.value
        and user_role != LitellmUserRoles.PROXY_ADMIN_VIEW_ONLY.value
    ):
        return False
    return True

