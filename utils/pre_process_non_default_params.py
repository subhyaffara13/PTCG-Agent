
def pre_process_non_default_params(
    passed_params: dict,
    special_params: dict,
    custom_llm_provider: str,
    additional_drop_params: Optional[List[str]],
    model: str,
    remove_sensitive_keys: bool = False,
    add_provider_specific_params: bool = False,
    provider_config: Optional[BaseConfig] = None,
) -> dict:
    """
    Pre-process non-default params to a standardized format
    """
    # retrieve all parameters passed to the function

    non_default_params = PreProcessNonDefaultParams.base_pre_process_non_default_params(
        passed_params=passed_params,
        special_params=special_params,
        custom_llm_provider=custom_llm_provider,
        additional_drop_params=additional_drop_params,
        default_param_values=DEFAULT_CHAT_COMPLETION_PARAM_VALUES,
        additional_endpoint_specific_params=["messages"],
    )

    if "response_format" in non_default_params:
        if provider_config is not None:
            non_default_params["response_format"] = (
                provider_config.get_json_schema_from_pydantic_object(
                    response_format=non_default_params["response_format"]
                )
            )
        else:
            non_default_params["response_format"] = type_to_response_format_param(
                response_format=non_default_params["response_format"]
            )

    if "tools" in non_default_params and isinstance(
        non_default_params, list
    ):  # fixes https://github.com/BerriAI/litellm/issues/4933
        tools = non_default_params["tools"]
        for (
            tool
        ) in (
            tools
        ):  # clean out 'additionalProperties = False'. Causes vertexai/gemini OpenAI API Schema errors - https://github.com/langchain-ai/langchainjs/issues/5240
            tool_function = tool.get("function", {})
            parameters = tool_function.get("parameters", None)
            if parameters is not None:
                new_parameters = copy.deepcopy(parameters)
                if (
                    "additionalProperties" in new_parameters
                    and new_parameters["additionalProperties"] is False
                ):
                    new_parameters.pop("additionalProperties", None)
                tool_function["parameters"] = new_parameters

    if add_provider_specific_params:
        non_default_params = add_provider_specific_params_to_optional_params(
            optional_params=non_default_params,
            passed_params=passed_params,
            custom_llm_provider=custom_llm_provider,
            openai_params=list(DEFAULT_CHAT_COMPLETION_PARAM_VALUES.keys()),
            additional_drop_params=additional_drop_params,
        )

    if remove_sensitive_keys:
        non_default_params = remove_sensitive_keys_from_dict(non_default_params)
    return non_default_params

