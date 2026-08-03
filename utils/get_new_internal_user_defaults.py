from typing import Optional

def get_new_internal_user_defaults(
    user_id: str, user_email: Optional[str] = None
) -> dict:
    user_info = litellm.default_internal_user_params or {}

    returned_dict: SSOUserDefinedValues = {
        "models": user_info.get("models") or [],
        "max_budget": user_info.get("max_budget", litellm.max_internal_user_budget),
        "budget_duration": user_info.get(
            "budget_duration", litellm.internal_user_budget_duration
        ),
        "user_email": user_email or user_info.get("user_email", None),
        "user_id": user_id,
        "user_role": "internal_user",
    }

    non_null_dict = {}
    for k, v in returned_dict.items():
        if v is not None:
            non_null_dict[k] = v
    return non_null_dict

