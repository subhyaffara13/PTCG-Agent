
def _apply_prompt_management_to_responses_call(
    input: Union[str, ResponseInputParam],
    model: str,
    custom_llm_provider: Optional[str],
    litellm_logging_obj: Optional[LiteLLMLoggingObj],
    kwargs: Dict[str, Any],
    local_vars: Dict[str, Any],
) -> tuple[Union[str, ResponseInputParam], str, Optional[str]]:
    async_merged = kwargs.pop("_async_prompt_merged_params", None)
    if async_merged is not None:
        for key, value in async_merged.items():
            local_vars[key] = value
        return input, model, custom_llm_provider

    prompt_id = cast(Optional[str], kwargs.get("prompt_id", None))
    prompt_variables = cast(Optional[dict], kwargs.get("prompt_variables", None))
    original_model = model

    if isinstance(input, str):
        client_input: List[AllMessageValues] = [{"role": "user", "content": input}]
    else:
        client_input = [
            item  # type: ignore[misc]
            for item in input
            if isinstance(item, dict) and "role" in item
        ]

    if isinstance(
        litellm_logging_obj, LiteLLMLoggingObj
    ) and litellm_logging_obj.should_run_prompt_management_hooks(
        prompt_id=prompt_id, non_default_params=kwargs
    ):
        (
            model,
            merged_input,
            merged_optional_params,
        ) = litellm_logging_obj.get_chat_completion_prompt(
            model=model,
            messages=client_input,
            non_default_params=kwargs,
            prompt_id=prompt_id,
            prompt_variables=prompt_variables,
            prompt_label=kwargs.get("prompt_label", None),
            prompt_version=kwargs.get("prompt_version", None),
        )
        input = cast(Union[str, ResponseInputParam], merged_input)
        local_vars["input"] = input
        local_vars["model"] = model
        if model != original_model:
            _, custom_llm_provider, _, _ = litellm.get_llm_provider(model=model)
            local_vars["custom_llm_provider"] = custom_llm_provider
        for key, value in merged_optional_params.items():
            local_vars[key] = value

    return input, model, custom_llm_provider

