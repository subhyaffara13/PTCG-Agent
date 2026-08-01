
def get_direct_access_models(
    user_db_object: LiteLLM_UserTable,
    llm_router: Router,
) -> List[str]:
    """
    Get all models that user has direct access to
    """

    direct_access_models: List[str] = []
    for model in user_db_object.models:
        deployments = llm_router.get_model_list(model_name=model)
        if deployments is not None:
            for deployment in deployments:
                model_id = deployment.get("model_info", {}).get("id", None)
                if model_id is not None:
                    direct_access_models.append(model_id)
    return direct_access_models

