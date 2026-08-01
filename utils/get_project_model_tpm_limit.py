
def get_project_model_tpm_limit(
    user_api_key_dict: UserAPIKeyAuth,
) -> Optional[Dict[str, int]]:
    if user_api_key_dict.project_metadata:
        return user_api_key_dict.project_metadata.get("model_tpm_limit")
    return None

