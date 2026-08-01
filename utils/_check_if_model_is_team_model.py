
def _check_if_model_is_team_model(
    models: List[DeploymentTypedDict], user_row: LiteLLM_UserTable
) -> List[Dict]:
    """
    Check if model is a team model

    Check if user is a member of the team that the model belongs to
    """

    user_team_models: List[Dict] = []
    for model in models:
        model_team_id = model.get("model_info", {}).get("team_id", None)

        if model_team_id is not None:
            if model_team_id in user_row.teams:
                user_team_models.append(cast(Dict, model))

    return user_team_models

