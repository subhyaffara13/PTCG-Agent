
def _update_model_if_team_alias_exists(
    data: dict,
    user_api_key_dict: UserAPIKeyAuth,
) -> None:
    """
    Update the model if the team alias exists

    If a alias map has been set on a team, then we want to make the request with the model the team alias is pointing to

    eg.
        - user calls `gpt-4o`
        - team.model_alias_map = {
            "gpt-4o": "gpt-4o-team-1"
        }
        - requested_model = "gpt-4o-team-1"

    Note: model_aliases for team models are deprecated. This function only applies
    to legacy non-team-scoped aliases. Team-scoped deployments use team_public_model_name
    and are resolved via map_team_model in route_llm_request.
    """
    _model = data.get("model")
    if (
        _model
        and user_api_key_dict.team_model_aliases
        and _model in user_api_key_dict.team_model_aliases
    ):
        from litellm.proxy.proxy_server import llm_router

        # Skip alias rewrite if this model resolves to team-specific deployments
        # (team models use team_public_model_name, not model_aliases)
        aliased_target = user_api_key_dict.team_model_aliases[_model]

        # Optional bypass for stale aliases from pre-PR deployments:
        # only enabled via feature flag to preserve backwards compatibility.
        # Cached at module level to avoid hot-path secret lookups on every request.
        global _ENABLE_TEAM_STALE_ALIAS_BYPASS
        if _ENABLE_TEAM_STALE_ALIAS_BYPASS is None:
            _ENABLE_TEAM_STALE_ALIAS_BYPASS = get_secret_bool(
                "LITELLM_ENABLE_TEAM_STALE_ALIAS_BYPASS", False
            )
        enable_stale_alias_bypass = _ENABLE_TEAM_STALE_ALIAS_BYPASS
        # Check if the alias points to a team-scoped UUID name
        # (format: "model_name_{team_id}_{uuid}")
        is_stale_team_alias = aliased_target.startswith(
            f"model_name_{user_api_key_dict.team_id}_"
        )
        if is_stale_team_alias and llm_router:
            # This is a stale alias from pre-PR deployments.
            # Check if current team deployments exist for the public name.
            key = (user_api_key_dict.team_id, _model)
            if key in llm_router.team_model_to_deployment_indices:
                if enable_stale_alias_bypass:
                    # Team deployments exist; skip stale alias
                    return
                warning_key = f"{user_api_key_dict.team_id}:{_model}:{aliased_target}"
                if warning_key not in _STALE_TEAM_ALIAS_WARNING_KEYS:
                    _STALE_TEAM_ALIAS_WARNING_KEYS[warning_key] = None
                    while (
                        len(_STALE_TEAM_ALIAS_WARNING_KEYS)
                        > _MAX_STALE_ALIAS_WARNING_KEYS
                    ):
                        _STALE_TEAM_ALIAS_WARNING_KEYS.popitem(last=False)
                    verbose_proxy_logger.warning(
                        "Stale team model alias detected for model='%s', team_id='%s'. "
                        "New sibling deployments may be unreachable. "
                        "Set LITELLM_ENABLE_TEAM_STALE_ALIAS_BYPASS=true to enable "
                        "team-scoped sibling routing.",
                        _sanitize_for_log(_model),
                        user_api_key_dict.team_id,
                    )

        data["model"] = aliased_target
    return

