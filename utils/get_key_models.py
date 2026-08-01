
def get_key_models(
    user_api_key_dict: UserAPIKeyAuth,
    proxy_model_list: List[str],
    model_access_groups: Dict[str, List[str]],
    include_model_access_groups: Optional[bool] = False,
    only_model_access_groups: Optional[bool] = False,
) -> List[str]:
    """
    Returns:
    - List of model name strings
    - Empty list if no models set
    - If model_access_groups is provided, only return models that are in the access groups
    - If include_model_access_groups is True, it includes the 'keys' of the model_access_groups
      in the response - {"beta-models": ["gpt-4", "claude-v1"]} -> returns 'beta-models'
    """
    all_models: List[str] = []
    if len(user_api_key_dict.models) > 0:
        all_models = list(
            user_api_key_dict.models
        )  # copy to avoid mutating cached objects
        if (
            SpecialModelNames.all_team_models.value in all_models
            and user_api_key_dict.team_id is not None
        ):
            all_models = list(
                user_api_key_dict.team_models
            )  # copy to avoid mutating cached objects
        if SpecialModelNames.all_proxy_models.value in all_models:
            all_models = list(proxy_model_list)  # copy to avoid mutating caller's list
            if include_model_access_groups:
                all_models.extend(model_access_groups.keys())

    all_models = _get_models_from_access_groups(
        model_access_groups=model_access_groups,
        all_models=all_models,
        include_model_access_groups=include_model_access_groups,
    )

    # deduplicate while preserving order
    all_models = list(dict.fromkeys(all_models))

    verbose_proxy_logger.debug("ALL KEY MODELS - {}".format(len(all_models)))
    return all_models

