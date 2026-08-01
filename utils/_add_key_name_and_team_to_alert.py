
def _add_key_name_and_team_to_alert(request_info: str, metadata: dict) -> str:
    """
    Internal helper function for litellm proxy
    Add the Key Name + Team Name to the error
    Only gets added if the metadata contains the user_api_key_alias and user_api_key_team_alias

    [Non-Blocking helper function]
    """
    try:
        _api_key_name = metadata.get("user_api_key_alias", None)
        _user_api_key_team_alias = metadata.get("user_api_key_team_alias", None)
        if _api_key_name is not None:
            request_info = (
                f"\n\nKey Name: `{_api_key_name}`\nTeam: `{_user_api_key_team_alias}`"
                + request_info
            )

        return request_info
    except Exception:
        return request_info

