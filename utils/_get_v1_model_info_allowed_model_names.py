
def _get_v1_model_info_allowed_model_names(
    user_api_key_dict: UserAPIKeyAuth,
    llm_router: Router,
) -> Optional[Set[str]]:
    """Return key/team allowlisted public model names, or None if unrestricted."""
    model_access_groups = llm_router.get_model_access_groups()
    proxy_model_list = llm_router.get_model_names()
    key_models = get_key_models(
        user_api_key_dict=user_api_key_dict,
        proxy_model_list=proxy_model_list,
        model_access_groups=model_access_groups,
    )
    team_models = get_team_models(
        team_models=user_api_key_dict.team_models,
        proxy_model_list=proxy_model_list,
        model_access_groups=model_access_groups,
    )
    if not key_models and not team_models:
        return None
    return set(
        get_complete_model_list(
            key_models=key_models,
            team_models=team_models,
            proxy_model_list=proxy_model_list,
            user_model=user_model,
            infer_model_from_keys=general_settings.get("infer_model_from_keys", False),
            llm_router=llm_router,
            return_wildcard_routes=False,
        )
    )

