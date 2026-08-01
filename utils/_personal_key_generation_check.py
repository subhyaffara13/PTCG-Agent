
def _personal_key_generation_check(
    user_api_key_dict: UserAPIKeyAuth, data: GenerateKeyRequest
):
    if (
        litellm.key_generation_settings is None
        or litellm.key_generation_settings.get("personal_key_generation") is None
    ):
        return True

    _personal_key_generation = litellm.key_generation_settings["personal_key_generation"]  # type: ignore

    _personal_key_membership_check(
        user_api_key_dict,
        personal_key_generation=_personal_key_generation,
    )

    _key_generation_required_param_check(
        data,
        _personal_key_generation.get("required_params"),
    )

    return True

