from typing import Dict, List, Optional, Union

def _can_object_call_model(
    model: Union[str, List[str]],
    llm_router: Optional[Router],
    models: List[str],
    team_model_aliases: Optional[Dict[str, str]] = None,
    team_id: Optional[str] = None,
    object_type: Literal["user", "team", "key", "org", "project"] = "user",
    fallback_depth: int = 0,
) -> Literal[True]:
    """
    Checks if token can call a given model

    Args:
        - model: str
        - llm_router: Optional[Router]
        - models: List[str]
        - team_model_aliases: Optional[Dict[str, str]]
        - object_type: Literal["user", "team", "key", "org"]. We use the object type to raise the correct exception type

    Returns:
        - True: if token allowed to call model

    Raises:
        - Exception: If token not allowed to call model
    """
    if fallback_depth >= DEFAULT_MAX_RECURSE_DEPTH:
        raise Exception(
            "Unable to parse model, max fallback depth exceeded - received model: {}".format(
                model
            )
        )
    if isinstance(model, list):
        for m in model:
            _can_object_call_model(
                model=m,
                llm_router=llm_router,
                models=models,
                team_model_aliases=team_model_aliases,
                team_id=team_id,
                object_type=object_type,
                fallback_depth=fallback_depth + 1,
            )
        return True

    potential_models = [model]
    if model in litellm.model_alias_map:
        potential_models.append(litellm.model_alias_map[model])
    elif llm_router and model in llm_router.model_group_alias:
        _model = llm_router._get_model_from_alias(model)
        if _model:
            potential_models.append(_model)

    ## check model access for alias + underlying model - allow if either is in allowed models
    for m in potential_models:
        if _check_model_access_helper(
            model=m,
            llm_router=llm_router,
            models=models,
            team_model_aliases=team_model_aliases,
            team_id=team_id,
        ):
            return True

    raise ProxyException(
        message=f"{object_type} not allowed to access model. This {object_type} can only access models={models}. Tried to access {model}",
        type=ProxyErrorTypes.get_model_access_error_type_for_object(
            object_type=object_type
        ),
        param="model",
        code=status.HTTP_403_FORBIDDEN,
    )

