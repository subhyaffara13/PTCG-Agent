
def _allows_litellm_changed_by_header(user_api_key_dict: UserAPIKeyAuth) -> bool:
    for admin_metadata in (user_api_key_dict.metadata, user_api_key_dict.team_metadata):
        if (
            isinstance(admin_metadata, dict)
            and admin_metadata.get(ALLOW_LITELLM_CHANGED_BY_HEADER_METADATA_KEY) is True
        ):
            return True
    return False

