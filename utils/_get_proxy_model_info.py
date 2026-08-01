
def _get_proxy_model_info(model: dict) -> dict:
    # provided model_info in config.yaml
    model_info = model.get("model_info", {})

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
    # don't return the llm credentials
    model = remove_sensitive_info_from_deployment(
        deployment_dict=model, excluded_keys={"litellm_credential_name"}
    )

    return _translate_model_name_for_response(model)

