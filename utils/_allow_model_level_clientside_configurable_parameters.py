
def _allow_model_level_clientside_configurable_parameters(
    model: str, param: str, request_body_value: Any, llm_router: Optional[Router]
) -> bool:
    """
    Check if model is allowed to use configurable client-side params
    - get matching model
    - check if 'clientside_configurable_parameters' is set for model
    -
    """
    if llm_router is None:
        return False
    # check if model is set
    model_info = llm_router.get_model_group_info(model_group=model)
    if model_info is None:
        # check if wildcard model is set
        if model.split("/", 1)[0] in provider_list:
            model_info = llm_router.get_model_group_info(
                model_group=model.split("/", 1)[0]
            )

    if model_info is None:
        return False

    if model_info is None or model_info.configurable_clientside_auth_params is None:
        return False

    return _is_param_allowed(
        param=param,
        request_body_value=request_body_value,
        configurable_clientside_auth_params=model_info.configurable_clientside_auth_params,
    )

