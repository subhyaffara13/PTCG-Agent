from typing import Optional

def _personal_key_membership_check(
    user_api_key_dict: UserAPIKeyAuth,
    personal_key_generation: Optional[PersonalUIKeyGenerationConfig],
):
    if (
        personal_key_generation is None
        or "allowed_user_roles" not in personal_key_generation
    ):
        return True

    if user_api_key_dict.user_role not in personal_key_generation["allowed_user_roles"]:
        raise HTTPException(
            status_code=400,
            detail=f"Personal key creation has been restricted by admin. Allowed roles={litellm.key_generation_settings['personal_key_generation']['allowed_user_roles']}. Your role={user_api_key_dict.user_role}",  # type: ignore
        )

    return True

