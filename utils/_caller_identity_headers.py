
def _caller_identity_headers(user_api_key_dict: UserAPIKeyAuth) -> Dict[str, str]:
    headers: Dict[str, str] = {}
    if user_api_key_dict.user_id:
        headers["X-LiteLLM-User-Id"] = user_api_key_dict.user_id
    if user_api_key_dict.team_id:
        headers["X-LiteLLM-Team-Id"] = user_api_key_dict.team_id
    return headers

