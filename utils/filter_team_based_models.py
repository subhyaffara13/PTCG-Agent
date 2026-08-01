
def filter_team_based_models(
    healthy_deployments: Union[List[Dict], Dict],
    request_kwargs: Optional[Dict] = None,
) -> Union[List[Dict], Dict]:
    """
    If a model has a team_id

    Only use if request is from that team
    """
    if request_kwargs is None:
        return healthy_deployments

    metadata = request_kwargs.get("metadata") or {}
    litellm_metadata = request_kwargs.get("litellm_metadata") or {}
    request_team_id = metadata.get("user_api_key_team_id") or litellm_metadata.get(
        "user_api_key_team_id"
    )
    ids_to_remove = set()
    if isinstance(healthy_deployments, dict):
        return healthy_deployments
    for deployment in healthy_deployments:
        _model_info = deployment.get("model_info") or {}
        model_team_id = _model_info.get("team_id")
        if model_team_id is None:
            continue
        if model_team_id != request_team_id:
            ids_to_remove.add(_model_info.get("id"))

    return [
        deployment
        for deployment in healthy_deployments
        if deployment.get("model_info", {}).get("id") not in ids_to_remove
    ]

