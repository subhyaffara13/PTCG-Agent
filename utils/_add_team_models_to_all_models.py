
def _add_team_models_to_all_models(
    team_db_objects_typed: List[LiteLLM_TeamTable],
    llm_router: Router,
) -> Dict[str, Set[str]]:
    """
    Add team models to all models
    """
    team_models: Dict[str, Set[str]] = {}

    for team_object in team_db_objects_typed:
        if (
            not team_object.models  # None or empty list = all model access
            or SpecialModelNames.all_proxy_models.value in team_object.models
        ):
            model_list = llm_router.get_model_list()
            if model_list is not None:
                for model in model_list:
                    model_id = model.get("model_info", {}).get("id", None)
                    if model_id is None:
                        continue
                    # if team model id set, check if team id in user_teams
                    team_model_id = model.get("model_info", {}).get("team_id", None)
                    can_add_model = False
                    if team_model_id is None:
                        can_add_model = True
                    elif team_model_id in team_object.team_id:
                        can_add_model = True

                    if can_add_model:
                        team_models.setdefault(model_id, set()).add(team_object.team_id)
        else:
            for model_name in team_object.models:
                _models = llm_router.get_model_list(
                    model_name=model_name, team_id=team_object.team_id
                )
                if _models is not None:
                    for model in _models:
                        model_id = model.get("model_info", {}).get("id", None)
                        if model_id is not None:
                            team_models.setdefault(model_id, set()).add(
                                team_object.team_id
                            )
    return team_models

