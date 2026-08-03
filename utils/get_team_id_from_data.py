from typing import Optional

def get_team_id_from_data(data: dict) -> Optional[str]:
    """
    Get the team id from the data's metadata or litellm_metadata params.
    """
    if (
        "metadata" in data
        and data["metadata"] is not None
        and "user_api_key_team_id" in data["metadata"]
    ):
        return data["metadata"].get("user_api_key_team_id")
    elif (
        "litellm_metadata" in data
        and data["litellm_metadata"] is not None
        and "user_api_key_team_id" in data["litellm_metadata"]
    ):
        return data["litellm_metadata"].get("user_api_key_team_id")
    return None

