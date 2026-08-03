from typing import Dict, List, Optional, Set

def get_team_models(
    team_models: List[str],
    proxy_model_list: List[str],
    model_access_groups: Dict[str, List[str]],
    include_model_access_groups: Optional[bool] = False,
) -> List[str]:
    """
    Returns:
    - List of model name strings
    - Empty list if no models set
    - If model_access_groups is provided, only return models that are in the access groups
    """
    all_models_set: Set[str] = set()
    if len(team_models) > 0:
        all_models_set.update(team_models)
        if SpecialModelNames.all_team_models.value in all_models_set:
            all_models_set.update(team_models)
        if SpecialModelNames.all_proxy_models.value in all_models_set:
            all_models_set.update(proxy_model_list)
            if include_model_access_groups:
                all_models_set.update(model_access_groups.keys())

    all_models = _get_models_from_access_groups(
        model_access_groups=model_access_groups,
        all_models=list(all_models_set),
        include_model_access_groups=include_model_access_groups,
    )

    # deduplicate while preserving order
    all_models = list(dict.fromkeys(all_models))

    verbose_proxy_logger.debug("ALL TEAM MODELS - {}".format(len(all_models)))
    return all_models

