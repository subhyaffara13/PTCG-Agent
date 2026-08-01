
def _key_or_team_metadata_flag_is_true(
    user_api_key_dict: UserAPIKeyAuth,
    metadata_key: str,
) -> bool:
    for admin_metadata in (user_api_key_dict.metadata, user_api_key_dict.team_metadata):
        if (
            isinstance(admin_metadata, dict)
            and admin_metadata.get(metadata_key) is True
        ):
            return True
    return False

