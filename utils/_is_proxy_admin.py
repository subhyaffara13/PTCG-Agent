
def _is_proxy_admin(user_api_key_dict: UserAPIKeyAuth) -> bool:
    return (
        user_api_key_dict.user_role == LitellmUserRoles.PROXY_ADMIN
        or user_api_key_dict.user_role == LitellmUserRoles.PROXY_ADMIN.value
    )


def _is_proxy_admin(user_api_key_dict: UserAPIKeyAuth) -> bool:
    """
    Return True if the caller has a proxy-admin role (full or view-only).

    user_role on UserAPIKeyAuth can be either a LitellmUserRoles enum or its
    string value depending on how the auth path constructed the object, so we
    compare against the raw value rather than the enum identity.
    """
    role = user_api_key_dict.user_role
    if role is None:
        return False
    role_value = role.value if hasattr(role, "value") else role
    return role_value in _PROXY_ADMIN_ROLES


def _is_proxy_admin(user_api_key_dict: UserAPIKeyAuth) -> bool:
    return (
        user_api_key_dict.user_role == LitellmUserRoles.PROXY_ADMIN
        or user_api_key_dict.user_role == LitellmUserRoles.PROXY_ADMIN.value
    )

