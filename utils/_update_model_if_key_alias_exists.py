
def _update_model_if_key_alias_exists(
    data: dict,
    user_api_key_dict: UserAPIKeyAuth,
) -> None:
    """
    Update the model if the key alias exists

    If an alias map has been set on a key, then we want to make the request with the model the key alias is pointing to

    eg.
        - user calls `modelAlias`
        - key.aliases = {
            "modelAlias": "xai/grok-4-fast-non-reasoning"
        }
        - requested_model = "xai/grok-4-fast-non-reasoning"
    """
    _model = data.get("model")
    if (
        _model
        and user_api_key_dict.aliases
        and isinstance(user_api_key_dict.aliases, dict)
        and _model in user_api_key_dict.aliases
    ):
        data["model"] = user_api_key_dict.aliases[_model]
    return

