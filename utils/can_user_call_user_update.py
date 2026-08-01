
def can_user_call_user_update(
    user_api_key_dict: UserAPIKeyAuth,
    user_info: LiteLLM_UserTable,
) -> bool:
    """
    Helper to check if the user has access to the key's info
    """
    if user_api_key_dict.user_role == LitellmUserRoles.PROXY_ADMIN.value:
        return True
    elif user_api_key_dict.user_id == user_info.user_id:
        return True
    return False

