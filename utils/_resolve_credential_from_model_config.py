
def _resolve_credential_from_model_config(
    model_name: str,
    project_model_config: Optional[dict],
    team_model_config: Optional[dict],
    pre_alias_model_name: Optional[str] = None,
    provider: Optional[str] = None,
) -> Optional[str]:
    """
    Walk the precedence chain and return the first matching credential name.

    Checks (in order):
    1. project_model_config[model_name][provider] — project model-specific
    2. project_model_config[pre_alias_model_name][provider] — project pre-alias
    3. project_model_config["defaultconfig"][provider] — project default
    4. team_model_config[model_name][provider] — team model-specific
    5. team_model_config[pre_alias_model_name][provider] — team pre-alias
    6. team_model_config["defaultconfig"][provider] — team default

    When a model-specific entry exists but contains no litellm_credentials,
    the function falls through to defaultconfig. This is intentional —
    an entry without litellm_credentials is treated as incomplete config,
    not as an explicit "no override" signal.
    """
    # Build the list of model names to try (post-alias first, then pre-alias)
    model_names_to_try = [model_name]
    if pre_alias_model_name and pre_alias_model_name != model_name:
        model_names_to_try.append(pre_alias_model_name)

    for model_config in (project_model_config, team_model_config):
        if not model_config or not isinstance(model_config, dict):
            continue

        # Model-specific check (try resolved name, then pre-alias name)
        for name in model_names_to_try:
            model_entry = model_config.get(name)
            if model_entry:
                credential_name = _extract_credential_from_entry(
                    model_entry, provider=provider
                )
                if credential_name:
                    return credential_name
                _safe_name = str(name).replace("\n", "").replace("\r", "")
                verbose_proxy_logger.debug(
                    "model_config entry '%s' found but has no litellm_credentials, "
                    "trying next candidate",
                    _safe_name,
                )

        # Default check
        default_entry = model_config.get("defaultconfig")
        if default_entry:
            credential_name = _extract_credential_from_entry(
                default_entry, provider=provider
            )
            if credential_name:
                return credential_name

    return None

