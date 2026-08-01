
def _check_model_access_helper(
    model: str,
    llm_router: Optional[Router],
    models: List[str],
    team_model_aliases: Optional[Dict[str, str]] = None,
    team_id: Optional[str] = None,
) -> bool:
    ## check if model in allowed model names
    from collections import defaultdict

    access_groups: Dict[str, List[str]] = defaultdict(list)

    if llm_router:
        access_groups = llm_router.get_model_access_groups(
            model_name=model, team_id=team_id
        )

    if (
        len(access_groups) > 0 and llm_router is not None
    ):  # check if token contains any model access groups
        for idx, m in enumerate(
            models
        ):  # loop token models, if any of them are an access group add the access group
            if m in access_groups:
                return True

    # Filter out models that are access_groups
    filtered_models = [m for m in models if m not in access_groups]

    if _model_in_team_aliases(model=model, team_model_aliases=team_model_aliases):
        return True

    if _model_matches_any_wildcard_pattern_in_list(
        model=model, allowed_model_list=filtered_models
    ):
        return True

    all_model_access: bool = False

    if (len(filtered_models) == 0 and len(models) == 0) or "*" in filtered_models:
        all_model_access = True

    if SpecialModelNames.all_proxy_models.value in filtered_models:
        all_model_access = True

    if model is not None and model not in filtered_models and all_model_access is False:
        return False
    return True

