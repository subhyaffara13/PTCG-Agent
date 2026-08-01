
def get_disabled_non_admin_personal_key_creation():
    key_generation_settings = litellm.key_generation_settings
    if key_generation_settings is None:
        return False
    personal_key_generation = (
        key_generation_settings.get("personal_key_generation") or {}
    )
    allowed_user_roles = personal_key_generation.get("allowed_user_roles") or []
    return bool("proxy_admin" in allowed_user_roles)

