
def get_complete_model_list(
    key_models: List[str],
    team_models: List[str],
    proxy_model_list: List[str],
    user_model: Optional[str],
    infer_model_from_keys: Optional[bool],
    return_wildcard_routes: Optional[bool] = False,
    llm_router: Optional[Router] = None,
    model_access_groups: Dict[str, List[str]] = {},
    include_model_access_groups: Optional[bool] = False,
    only_model_access_groups: Optional[bool] = False,
    team_id: Optional[str] = None,
) -> List[str]:
    """Logic for returning complete model list for a given key + team pair"""

    """
    - If key list is empty -> defer to team list
    - If team list is empty -> defer to proxy model list

    If list contains wildcard -> return known provider models
    """

    unique_models = []

    def append_unique(models):
        for model in models:
            if model not in unique_models:
                unique_models.append(model)

    if key_models:
        append_unique(key_models)
    elif team_models:
        append_unique(team_models)
    else:
        append_unique(proxy_model_list)
        if include_model_access_groups:
            append_unique(list(model_access_groups.keys()))  # TODO: keys order

        if user_model:
            append_unique([user_model])

        if infer_model_from_keys:
            valid_models = get_valid_models()
            append_unique(valid_models)

    if only_model_access_groups:
        model_access_groups_to_return: List[str] = []
        for model in unique_models:
            if model in model_access_groups:
                model_access_groups_to_return.append(model)
        return model_access_groups_to_return

    all_wildcard_models = _get_wildcard_models(
        unique_models=unique_models,
        return_wildcard_routes=return_wildcard_routes,
        llm_router=llm_router,
        team_id=team_id,
    )

    complete_model_list = unique_models + all_wildcard_models

    return complete_model_list

