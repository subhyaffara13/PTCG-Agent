from typing import Dict, Optional

def get_team_model_tpm_limit(
    user_api_key_dict: UserAPIKeyAuth,
) -> Optional[Dict[str, int]]:
    if user_api_key_dict.team_metadata:
        return user_api_key_dict.team_metadata.get("model_tpm_limit")
    return None

