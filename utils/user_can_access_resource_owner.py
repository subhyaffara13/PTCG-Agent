
def user_can_access_resource_owner(
    owner: Optional[str],
    user_api_key_dict: Optional[UserAPIKeyAuth],
) -> bool:
    if user_api_key_dict is None:
        return True
    if is_proxy_admin(user_api_key_dict):
        return True
    if owner is None:
        return False
    return owner in get_resource_owner_scopes(user_api_key_dict)

