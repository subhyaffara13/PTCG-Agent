
def is_proxy_admin(user_api_key_dict: Optional[UserAPIKeyAuth]) -> bool:
    if user_api_key_dict is None:
        return False

    return (
        user_api_key_dict.user_role == LitellmUserRoles.PROXY_ADMIN
        or user_api_key_dict.user_role == LitellmUserRoles.PROXY_ADMIN.value
    )

