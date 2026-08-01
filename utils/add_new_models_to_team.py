
def add_new_models_to_team(
    team_obj: LiteLLM_TeamTable, new_models: List[str]
) -> List[str]:
    """
    Add new models to a team's allowed model list.
    """
    current_models = team_obj.models
    if (
        current_models is not None and len(current_models) == 0
    ):  # implies all model access
        current_models = [SpecialModelNames.all_proxy_models.value]
    else:
        current_models = team_obj.models
    updated_models = list(set(current_models + new_models))
    return updated_models

