
def _enrich_model_info_with_litellm_data(
    model: Dict[str, Any], debug: bool = False, llm_router: Optional[Router] = None
) -> Dict[str, Any]:
    """
    Enrich a model dictionary with litellm model info (pricing, context window, etc.)
    and remove sensitive information.

    Args:
        model: Model dictionary to enrich
        debug: Whether to include debug information like openai_client
        llm_router: Optional router instance for debug info

    Returns:
        Enriched model dictionary with sensitive info removed
    """
    # provided model_info in config.yaml
    model_info = model.get("model_info", {})
    if debug is True:
        _openai_client = "None"
        if llm_router is not None:
            _openai_client = (
                llm_router._get_client(deployment=model, kwargs={}, client_type="async")
                or "None"
            )
        else:
            _openai_client = "llm_router_is_None"
        openai_client = str(_openai_client)
        model["openai_client"] = openai_client

    # read litellm model_prices_and_context_window.json to get the following:
    # input_cost_per_token, output_cost_per_token, max_tokens
    litellm_model_info = get_litellm_model_info(model=model)

    # 2nd pass on the model, try seeing if we can find model in litellm model_cost map
    if litellm_model_info == {}:
        # use litellm_param model_name to get model_info
        litellm_params = model.get("litellm_params", {})
        litellm_model = litellm_params.get("model", None)
        try:
            litellm_model_info = litellm.get_model_info(model=litellm_model)
        except Exception:
            litellm_model_info = {}
    # 3rd pass on the model, try seeing if we can find model but without the "/" in model cost map
    if litellm_model_info == {}:
        # use litellm_param model_name to get model_info
        litellm_params = model.get("litellm_params", {})
        litellm_model = litellm_params.get("model", None)
        if litellm_model:
            split_model = litellm_model.split("/")
            if len(split_model) > 0:
                litellm_model = split_model[-1]
            try:
                litellm_model_info = litellm.get_model_info(
                    model=litellm_model, custom_llm_provider=split_model[0]
                )
            except Exception:
                litellm_model_info = {}
    for k, v in litellm_model_info.items():
        if k not in model_info:
            model_info[k] = v
    model["model_info"] = model_info
    # don't return the api key / vertex credentials
    # don't return the llm credentials
    model = remove_sensitive_info_from_deployment(
        model, excluded_keys={"litellm_credential_name"}
    )
    return model

