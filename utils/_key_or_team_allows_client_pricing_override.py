
def _key_or_team_allows_client_pricing_override(
    user_api_key_dict: UserAPIKeyAuth,
) -> bool:
    return _key_or_team_metadata_flag_is_true(
        user_api_key_dict=user_api_key_dict,
        metadata_key=_ALLOW_CLIENT_PRICING_OVERRIDE_METADATA_KEY,
    )

