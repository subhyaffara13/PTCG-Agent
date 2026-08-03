from typing import Optional

def _apply_credential_overrides_from_model_config(
    data: dict,
    user_api_key_dict: UserAPIKeyAuth,
    pre_alias_model_name: Optional[str] = None,
    llm_router: Optional[Router] = None,
) -> None:
    """
    Walk the model_config precedence chain in team/project metadata.
    If a matching credential is found, set api_base/api_key/api_version on data
    so they override deployment defaults in the router.

    Precedence (highest to lowest):
    1. Clientside credentials (already in data — skip if present)
    2. Project model-specific override
    3. Project default override (defaultconfig)
    4. Team model-specific override
    5. Team default override (defaultconfig)
    6. Deployment default (no action needed)
    """
    # Feature flag gate — disabled by default, opt in with litellm.enable_model_config_credential_overrides = True
    if not litellm.enable_model_config_credential_overrides:
        return

    # Respect clientside credentials — highest precedence
    if data.get("api_base") is not None or data.get("api_key") is not None:
        return

    model_name = data.get("model")
    if not model_name:
        return

    project_metadata = user_api_key_dict.project_metadata or {}
    team_metadata = user_api_key_dict.team_metadata or {}

    project_model_config = project_metadata.get("model_config")
    team_model_config = team_metadata.get("model_config")

    if not project_model_config and not team_model_config:
        return

    # Extract provider hint from model name (e.g. "azure/gpt-4" -> "azure").
    # When the user-facing name has no provider prefix, fall back to the
    # deployment's litellm_params so multi-provider defaultconfig entries
    # don't silently match the first dict key (#27516).
    provider: Optional[str] = None
    if "/" in model_name:
        provider = model_name.split("/", 1)[0]
    elif llm_router is not None:
        provider = _resolve_provider_from_deployment(
            llm_router=llm_router,
            model_name=model_name,
            pre_alias_model_name=pre_alias_model_name,
        )

    credential_name = _resolve_credential_from_model_config(
        model_name=model_name,
        project_model_config=project_model_config,
        team_model_config=team_model_config,
        pre_alias_model_name=pre_alias_model_name,
        provider=provider,
    )

    if not credential_name:
        return

    credential_values = CredentialAccessor.get_credential_values(credential_name)
    if not credential_values:
        _safe_cred = str(credential_name).replace("\n", "").replace("\r", "")
        verbose_proxy_logger.warning(
            "model_config references credential '%s' but it was not found or has no values",
            _safe_cred,
        )
        return

    # Apply credential overrides only for keys not already in the request
    for key in ("api_base", "api_key", "api_version"):
        if key in credential_values and key not in data:
            data[key] = credential_values[key]

    _safe_model = str(model_name).replace("\n", "").replace("\r", "")
    _safe_cred = str(credential_name).replace("\n", "").replace("\r", "")
    verbose_proxy_logger.debug(
        "Applied credential override '%s' for model '%s'",
        _safe_cred,
        _safe_model,
    )

