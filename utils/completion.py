
def completion(  # type: ignore
    model: str,
    # Optional OpenAI params: see https://platform.openai.com/docs/api-reference/chat/create
    messages: List = [],
    timeout: Optional[Union[float, str, httpx.Timeout]] = None,
    temperature: Optional[float] = None,
    top_p: Optional[float] = None,
    n: Optional[int] = None,
    stream: Optional[bool] = None,
    stream_options: Optional[dict] = None,
    stop=None,
    max_completion_tokens: Optional[int] = None,
    max_tokens: Optional[int] = None,
    modalities: Optional[List[ChatCompletionModality]] = None,
    prediction: Optional[ChatCompletionPredictionContentParam] = None,
    audio: Optional[ChatCompletionAudioParam] = None,
    presence_penalty: Optional[float] = None,
    frequency_penalty: Optional[float] = None,
    logit_bias: Optional[dict] = None,
    user: Optional[str] = None,
    # openai v1.0+ new params
    reasoning_effort: Optional[
        Literal["none", "minimal", "low", "medium", "high", "xhigh", "default"]
    ] = None,
    verbosity: Optional[Literal["low", "medium", "high"]] = None,
    response_format: Optional[Union[dict, Type[BaseModel]]] = None,
    seed: Optional[int] = None,
    tools: Optional[List] = None,
    tool_choice: Optional[Union[str, dict]] = None,
    logprobs: Optional[bool] = None,
    top_logprobs: Optional[int] = None,
    parallel_tool_calls: Optional[bool] = None,
    web_search_options: Optional[OpenAIWebSearchOptions] = None,
    include_server_side_tool_invocations: Optional[bool] = None,
    deployment_id=None,
    extra_headers: Optional[dict] = None,
    safety_identifier: Optional[str] = None,
    service_tier: Optional[str] = None,
    # soon to be deprecated params by OpenAI
    functions: Optional[List] = None,
    function_call: Optional[str] = None,
    # set api_base, api_version, api_key
    base_url: Optional[str] = None,
    api_version: Optional[str] = None,
    api_key: Optional[str] = None,
    model_list: Optional[list] = None,  # pass in a list of api_base,keys, etc.
    # Optional liteLLM function params
    thinking: Optional[AnthropicThinkingParam] = None,
    # Session management
    shared_session: Optional["ClientSession"] = None,
    # Per-request JSON schema validation (overrides litellm.enable_json_schema_validation)
    enable_json_schema_validation: Optional[bool] = None,
    **kwargs,
) -> Union[ModelResponse, CustomStreamWrapper]:
    """
    Perform a completion() using any of litellm supported llms (example gpt-4, gpt-3.5-turbo, claude-2, command-nightly)
    Parameters:
        model (str): The name of the language model to use for text completion. see all supported LLMs: https://docs.litellm.ai/docs/providers/
        messages (List): A list of message objects representing the conversation context (default is an empty list).

        OPTIONAL PARAMS
        functions (List, optional): A list of functions to apply to the conversation messages (default is an empty list).
        function_call (str, optional): The name of the function to call within the conversation (default is an empty string).
        temperature (float, optional): The temperature parameter for controlling the randomness of the output (default is 1.0).
        top_p (float, optional): The top-p parameter for nucleus sampling (default is 1.0).
        n (int, optional): The number of completions to generate (default is 1).
        stream (bool, optional): If True, return a streaming response (default is False).
        stream_options (dict, optional): A dictionary containing options for the streaming response. Only set this when you set stream: true.
        stop(string/list, optional): - Up to 4 sequences where the LLM API will stop generating further tokens.
        max_tokens (integer, optional): The maximum number of tokens in the generated completion (default is infinity).
        max_completion_tokens (integer, optional): An upper bound for the number of tokens that can be generated for a completion, including visible output tokens and reasoning tokens.
        modalities (List[ChatCompletionModality], optional): Output types that you would like the model to generate for this request.. You can use `["text", "audio"]`
        prediction (ChatCompletionPredictionContentParam, optional): Configuration for a Predicted Output, which can greatly improve response times when large parts of the model response are known ahead of time. This is most common when you are regenerating a file with only minor changes to most of the content.
        audio (ChatCompletionAudioParam, optional): Parameters for audio output. Required when audio output is requested with modalities: ["audio"]
        presence_penalty (float, optional): It is used to penalize new tokens based on their existence in the text so far.
        frequency_penalty: It is used to penalize new tokens based on their frequency in the text so far.
        logit_bias (dict, optional): Used to modify the probability of specific tokens appearing in the completion.
        user (str, optional):  A unique identifier representing your end-user. This can help the LLM provider to monitor and detect abuse.
        logprobs (bool, optional): Whether to return log probabilities of the output tokens or not. If true, returns the log probabilities of each output token returned in the content of message
        top_logprobs (int, optional): An integer between 0 and 5 specifying the number of most likely tokens to return at each token position, each with an associated log probability. logprobs must be set to true if this parameter is used.
        metadata (dict, optional): Pass in additional metadata to tag your completion calls - eg. prompt version, details, etc.
        api_base (str, optional): Base URL for the API (default is None).
        api_version (str, optional): API version (default is None).
        api_key (str, optional): API key (default is None).
        model_list (list, optional): List of api base, version, keys
        extra_headers (dict, optional): Additional headers to include in the request.

        LITELLM Specific Params
        mock_response (str, optional): If provided, return a mock completion response for testing or debugging purposes (default is None).
        custom_llm_provider (str, optional): Used for Non-OpenAI LLMs, Example usage for bedrock, set model="amazon.titan-tg1-large" and custom_llm_provider="bedrock"
        max_retries (int, optional): The number of retries to attempt (default is 0).
    Returns:
        ModelResponse: A response object containing the generated completion and associated metadata.

    Note:
        - This function is used to perform completions() using the specified language model.
        - It supports various optional parameters for customizing the completion behavior.
        - If 'mock_response' is provided, a mock completion response is returned for testing or debugging.
    """
    ### VALIDATE Request ###
    if model is None:
        raise ValueError("model param not passed in.")
    # validate messages
    messages = validate_and_fix_openai_messages(messages=messages)
    tools = validate_and_fix_openai_tools(tools=tools)
    # validate tool_choice
    tool_choice = validate_chat_completion_tool_choice(tool_choice=tool_choice)
    # validate optional params
    stop = validate_openai_optional_params(stop=stop)
    # normalize camelCase thinking keys (e.g. budgetTokens -> budget_tokens)
    thinking = validate_and_fix_thinking_param(thinking=thinking)

    ######### unpacking kwargs #####################
    args = locals()

    skip_mcp_handler = kwargs.pop("_skip_mcp_handler", False)
    if not skip_mcp_handler and tools:
        from litellm.responses.mcp.chat_completions_handler import acompletion_with_mcp
        from litellm.responses.mcp.litellm_proxy_mcp_handler import (
            LiteLLM_Proxy_MCP_Handler,
        )
        from litellm.types.llms.openai import ToolParam

        # Check if MCP tools are present (following responses pattern)
        # Cast tools to Optional[Iterable[ToolParam]] for type checking
        tools_for_mcp = cast(Optional[Iterable[ToolParam]], tools)
        if LiteLLM_Proxy_MCP_Handler._should_use_litellm_mcp_gateway(
            tools=tools_for_mcp
        ):
            # Return coroutine - acompletion will await it
            # completion() can return a coroutine when MCP tools are present, which acompletion() awaits
            return acompletion_with_mcp(  # type: ignore[return-value]
                model=model,
                messages=messages,
                functions=functions,
                function_call=function_call,
                timeout=timeout,
                temperature=temperature,
                top_p=top_p,
                n=n,
                stream=stream,
                stream_options=stream_options,
                stop=stop,
                max_tokens=max_tokens,
                max_completion_tokens=max_completion_tokens,
                modalities=modalities,
                prediction=prediction,
                audio=audio,
                presence_penalty=presence_penalty,
                frequency_penalty=frequency_penalty,
                logit_bias=logit_bias,
                user=user,
                response_format=response_format,
                seed=seed,
                tools=tools,
                tool_choice=tool_choice,
                parallel_tool_calls=parallel_tool_calls,
                logprobs=logprobs,
                top_logprobs=top_logprobs,
                deployment_id=deployment_id,
                reasoning_effort=reasoning_effort,
                verbosity=verbosity,
                safety_identifier=safety_identifier,
                service_tier=service_tier,
                base_url=base_url,
                api_version=api_version,
                api_key=api_key,
                model_list=model_list,
                extra_headers=extra_headers,
                thinking=thinking,
                web_search_options=web_search_options,
                shared_session=shared_session,
                enable_json_schema_validation=enable_json_schema_validation,
                **kwargs,
            )
    api_base = kwargs.get("api_base", None)
    mock_response: Optional[MOCK_RESPONSE_TYPE] = kwargs.get("mock_response", None)
    mock_tool_calls = kwargs.get("mock_tool_calls", None)
    mock_timeout = cast(Optional[bool], kwargs.get("mock_timeout", None))
    force_timeout = kwargs.get("force_timeout", 600)  ## deprecated
    logger_fn = kwargs.get("logger_fn", None)
    verbose = kwargs.get("verbose", False)
    custom_llm_provider = kwargs.get("custom_llm_provider", None)
    litellm_logging_obj = kwargs.get("litellm_logging_obj", None)
    id = kwargs.get("id", None)
    metadata = kwargs.get("metadata", None)
    model_info = kwargs.get("model_info", None)
    proxy_server_request = kwargs.get("proxy_server_request", None)
    fallbacks = kwargs.get("fallbacks", None)
    provider_specific_header = cast(
        Optional[ProviderSpecificHeader], kwargs.get("provider_specific_header", None)
    )
    headers = kwargs.get("headers", None) or extra_headers

    ensure_alternating_roles: Optional[bool] = kwargs.get(
        "ensure_alternating_roles", None
    )
    user_continue_message: Optional[ChatCompletionUserMessage] = kwargs.get(
        "user_continue_message", None
    )
    assistant_continue_message: Optional[ChatCompletionAssistantMessage] = kwargs.get(
        "assistant_continue_message", None
    )
    if headers is None:
        headers = {}
    if extra_headers is not None:
        headers.update(extra_headers)
    # Inject proxy auth headers if configured
    if litellm.proxy_auth is not None:
        try:
            proxy_headers = litellm.proxy_auth.get_auth_headers()
            headers.update(proxy_headers)
        except Exception as e:
            verbose_logger.warning(f"Failed to get proxy auth headers: {e}")
    num_retries = kwargs.get(
        "num_retries", None
    )  ## alt. param for 'max_retries'. Use this to pass retries w/ instructor.
    max_retries = kwargs.get("max_retries", None)
    cooldown_time = kwargs.get("cooldown_time", None)
    context_window_fallback_dict = kwargs.get("context_window_fallback_dict", None)
    organization = kwargs.get("organization", None)
    ### VERIFY SSL ###
    ssl_verify = kwargs.get("ssl_verify", None)
    ### CUSTOM MODEL COST ###
    input_cost_per_token = kwargs.get("input_cost_per_token", None)
    output_cost_per_token = kwargs.get("output_cost_per_token", None)
    input_cost_per_second = kwargs.get("input_cost_per_second", None)
    output_cost_per_second = kwargs.get("output_cost_per_second", None)
    ### CUSTOM PROMPT TEMPLATE ###
    initial_prompt_value = kwargs.get("initial_prompt_value", None)
    roles = kwargs.get("roles", None)
    final_prompt_value = kwargs.get("final_prompt_value", None)
    bos_token = kwargs.get("bos_token", None)
    eos_token = kwargs.get("eos_token", None)
    preset_cache_key = kwargs.get("preset_cache_key", None)
    hf_model_name = kwargs.get("hf_model_name", None)
    supports_system_message = kwargs.get("supports_system_message", None)
    base_model = kwargs.get("base_model", None) or (
        model_info.get("base_model") if isinstance(model_info, dict) else None
    )
    ### DISABLE FLAGS ###
    disable_add_transform_inline_image_block = kwargs.get(
        "disable_add_transform_inline_image_block", None
    )
    ### TEXT COMPLETION CALLS ###
    text_completion = kwargs.get("text_completion", False)
    atext_completion = kwargs.get("atext_completion", False)
    ### ASYNC CALLS ###
    acompletion = kwargs.get("acompletion", False)
    client = kwargs.get("client", None)
    ### Admin Controls ###
    no_log = kwargs.get("no-log", False)
    ### PROMPT MANAGEMENT ###
    prompt_id = cast(Optional[str], kwargs.get("prompt_id", None))
    prompt_variables = cast(Optional[dict], kwargs.get("prompt_variables", None))
    litellm_system_prompt = kwargs.get("litellm_system_prompt", None)
    ### COPY MESSAGES ### - related issue https://github.com/BerriAI/litellm/discussions/4489
    messages = get_completion_messages(
        messages=messages,
        ensure_alternating_roles=ensure_alternating_roles or False,
        user_continue_message=user_continue_message,
        assistant_continue_message=assistant_continue_message,
    )
    ######## end of unpacking kwargs ###########
    non_default_params = get_non_default_completion_params(kwargs=kwargs)
    litellm_params = {}  # used to prevent unbound var errors
    ## PROMPT MANAGEMENT HOOKS ##

    if isinstance(litellm_logging_obj, LiteLLMLoggingObj) and (
        litellm_logging_obj.should_run_prompt_management_hooks(
            prompt_id=prompt_id, non_default_params=non_default_params
        )
    ):
        (
            model,
            messages,
            optional_params,
        ) = litellm_logging_obj.get_chat_completion_prompt(
            model=model,
            messages=messages,
            non_default_params=non_default_params,
            prompt_id=prompt_id,
            prompt_variables=prompt_variables,
            prompt_label=kwargs.get("prompt_label", None),
            prompt_version=kwargs.get("prompt_version", None),
        )

    ### LITELLM SYSTEM PROMPT ###
    if litellm_system_prompt:
        messages = add_system_prompt_to_messages(
            messages=messages,
            system_prompt=litellm_system_prompt,
            merge_with_first_system=True,
        )

    try:
        if base_url is not None:
            api_base = base_url
        if num_retries is not None:
            max_retries = num_retries
        logging: LiteLLMLoggingObj = cast(LiteLLMLoggingObj, litellm_logging_obj)
        fallbacks = fallbacks or litellm.model_fallbacks
        if fallbacks is not None:
            return completion_with_fallbacks(**args)
        if model_list is not None:
            deployments = [
                m["litellm_params"] for m in model_list if m["model_name"] == model
            ]
            return litellm.batch_completion_models(deployments=deployments, **args)
        if litellm.model_alias_map and model in litellm.model_alias_map:
            model = litellm.model_alias_map[
                model
            ]  # update the model to the actual value if an alias has been passed in
        model_response = ModelResponse()
        setattr(model_response, "usage", litellm.Usage())
        if (
            kwargs.get("azure", False) is True
        ):  # don't remove flag check, to remain backwards compatible for repos like Codium
            custom_llm_provider = "azure"
        if deployment_id is not None:  # azure llms
            model = deployment_id
            custom_llm_provider = "azure"
        _supplemental_provider_params = {
            k: kwargs[k] for k in OPTIONAL_KWARGS_KEYS if k in kwargs
        }
        model, custom_llm_provider, dynamic_api_key, api_base = get_llm_provider(
            model=model,
            custom_llm_provider=custom_llm_provider,
            api_base=api_base,
            api_key=api_key,
            litellm_params=(
                GenericLiteLLMParams(**_supplemental_provider_params)
                if _supplemental_provider_params
                else None
            ),
        )

        ## RESPONSES API BRIDGE LOGIC ## - check early and normalize model name
        responses_api_model_info, model = responses_api_bridge_check(
            model=model,
            custom_llm_provider=custom_llm_provider,
            web_search_options=web_search_options,
        )

        if not _should_allow_input_examples(
            custom_llm_provider=custom_llm_provider, model=model
        ):
            tools = _drop_input_examples_from_tools(tools=tools)

        if provider_specific_header is not None:
            headers.update(
                ProviderSpecificHeaderUtils.get_provider_specific_headers(
                    provider_specific_header=provider_specific_header,
                    custom_llm_provider=custom_llm_provider,
                )
            )

        if model_response is not None and hasattr(model_response, "_hidden_params"):
            model_response._hidden_params["custom_llm_provider"] = custom_llm_provider
            model_response._hidden_params["region_name"] = kwargs.get(
                "aws_region_name", None
            )  # support region-based pricing for bedrock

        ### TIMEOUT LOGIC ###
        timeout = CompletionTimeout.resolve(
            timeout,
            kwargs,
            custom_llm_provider,
            global_timeout=getattr(litellm, "request_timeout", None),
            supports_httpx_timeout=supports_httpx_timeout,
        )

        ### REGISTER CUSTOM MODEL PRICING -- IF GIVEN ###
        if (
            input_cost_per_token is not None and output_cost_per_token is not None
        ) or input_cost_per_second is not None:
            litellm.register_model(
                {
                    f"{custom_llm_provider}/{model}": _build_custom_pricing_entry(
                        custom_llm_provider=custom_llm_provider,
                        kwargs=kwargs,
                        model_info=model_info,
                    )
                }
            )
        ### BUILD CUSTOM PROMPT TEMPLATE -- IF GIVEN ###
        custom_prompt_dict = {}  # type: ignore
        if (
            initial_prompt_value
            or roles
            or final_prompt_value
            or bos_token
            or eos_token
        ):
            custom_prompt_dict = {model: {}}
            if initial_prompt_value:
                custom_prompt_dict[model]["initial_prompt_value"] = initial_prompt_value
            if roles:
                custom_prompt_dict[model]["roles"] = roles
            if final_prompt_value:
                custom_prompt_dict[model]["final_prompt_value"] = final_prompt_value
            if bos_token:
                custom_prompt_dict[model]["bos_token"] = bos_token
            if eos_token:
                custom_prompt_dict[model]["eos_token"] = eos_token

        messages = update_messages_with_model_file_ids(
            messages=messages,
            model_id=kwargs.get("model_info", {}).get("id", None),
            model_file_id_mapping=cast(
                Dict[str, Dict[str, str]],
                kwargs.get("model_file_id_mapping") or {},
            ),
        )

        provider_config: Optional[BaseConfig] = None
        if custom_llm_provider is not None and custom_llm_provider in [
            provider.value for provider in LlmProviders
        ]:
            provider_config = ProviderConfigManager.get_provider_chat_config(
                model=model,
                provider=LlmProviders(custom_llm_provider),
                base_model=base_model,
            )

        if provider_config is not None:
            messages = provider_config.translate_developer_role_to_system_role(
                messages=messages
            )

        if (
            supports_system_message is not None
            and isinstance(supports_system_message, bool)
            and supports_system_message is False
        ):
            messages = map_system_message_pt(messages=messages)

        if dynamic_api_key is not None:
            api_key = dynamic_api_key
        # check if user passed in any of the OpenAI optional params
        optional_param_args = {
            "functions": functions,
            "function_call": function_call,
            "temperature": temperature,
            "top_p": top_p,
            "n": n,
            "stream": stream,
            "stream_options": stream_options,
            "stop": stop,
            "max_tokens": max_tokens,
            "max_completion_tokens": max_completion_tokens,
            "modalities": modalities,
            "prediction": prediction,
            "audio": audio,
            "presence_penalty": presence_penalty,
            "frequency_penalty": frequency_penalty,
            "logit_bias": logit_bias,
            "user": user,
            # params to identify the model
            "model": model,
            "custom_llm_provider": custom_llm_provider,
            "response_format": response_format,
            "seed": seed,
            "tools": tools,
            "tool_choice": tool_choice,
            "max_retries": max_retries,
            "logprobs": logprobs,
            "top_logprobs": top_logprobs,
            "api_version": api_version,
            "parallel_tool_calls": parallel_tool_calls,
            "messages": messages,
            "reasoning_effort": reasoning_effort,
            "thinking": thinking,
            "web_search_options": web_search_options,
            "include_server_side_tool_invocations": (
                include_server_side_tool_invocations
                if include_server_side_tool_invocations is not None
                else kwargs.get("include_server_side_tool_invocations")
            ),
            "safety_identifier": safety_identifier,
            "service_tier": service_tier,
            "allowed_openai_params": kwargs.get("allowed_openai_params"),
            "base_model": base_model,
        }
        optional_params = get_optional_params(
            **optional_param_args, **non_default_params
        )
        processed_non_default_params = pre_process_non_default_params(
            model=model,
            passed_params=optional_param_args,
            special_params=non_default_params,
            custom_llm_provider=custom_llm_provider,
            additional_drop_params=kwargs.get("additional_drop_params"),
            remove_sensitive_keys=True,
            add_provider_specific_params=True,
            provider_config=provider_config,
        )

        if litellm.add_function_to_prompt and optional_params.get(
            "functions_unsupported_model", None
        ):  # if user opts to add it to prompt, when API doesn't support function calling
            functions_unsupported_model = optional_params.pop(
                "functions_unsupported_model"
            )
            messages = function_call_prompt(
                messages=messages, functions=functions_unsupported_model
            )

        # For logging - save the values of the litellm-specific params passed in
        litellm_params = get_litellm_params(
            acompletion=acompletion,
            api_key=api_key,
            force_timeout=force_timeout,
            logger_fn=logger_fn,
            verbose=verbose,
            custom_llm_provider=custom_llm_provider,
            api_base=api_base,
            litellm_call_id=kwargs.get("litellm_call_id", None),
            model_alias_map=litellm.model_alias_map,
            completion_call_id=id,
            metadata=metadata,
            model_info=model_info,
            proxy_server_request=proxy_server_request,
            preset_cache_key=preset_cache_key,
            no_log=no_log,
            input_cost_per_second=input_cost_per_second,
            input_cost_per_token=input_cost_per_token,
            output_cost_per_second=output_cost_per_second,
            output_cost_per_token=output_cost_per_token,
            cooldown_time=cooldown_time,
            text_completion=kwargs.get("text_completion"),
            azure_ad_token_provider=kwargs.get("azure_ad_token_provider"),
            user_continue_message=kwargs.get("user_continue_message"),
            base_model=base_model,
            litellm_trace_id=kwargs.get("litellm_trace_id"),
            litellm_session_id=kwargs.get("litellm_session_id"),
            hf_model_name=hf_model_name,
            custom_prompt_dict=custom_prompt_dict,
            litellm_metadata=kwargs.get("litellm_metadata"),
            disable_add_transform_inline_image_block=disable_add_transform_inline_image_block,
            drop_params=kwargs.get("drop_params"),
            prompt_id=prompt_id,
            prompt_variables=prompt_variables,
            ssl_verify=ssl_verify,
            merge_reasoning_content_in_choices=kwargs.get(
                "merge_reasoning_content_in_choices", None
            ),
            use_litellm_proxy=kwargs.get("use_litellm_proxy", False),
            api_version=api_version,
            azure_ad_token=kwargs.get("azure_ad_token"),
            tenant_id=kwargs.get("tenant_id"),
            client_id=kwargs.get("client_id"),
            client_secret=kwargs.get("client_secret"),
            azure_username=kwargs.get("azure_username"),
            azure_password=kwargs.get("azure_password"),
            azure_scope=kwargs.get("azure_scope"),
            max_retries=max_retries,
            timeout=timeout,
            litellm_request_debug=kwargs.get("litellm_request_debug", False),
            tpm=kwargs.get("tpm"),
            rpm=kwargs.get("rpm"),
            use_xai_oauth=kwargs.get("use_xai_oauth", False),
            aws_bedrock_project_id=kwargs.get("aws_bedrock_project_id"),
        )
        cast(LiteLLMLoggingObj, logging).update_environment_variables(
            model=model,
            user=user,
            optional_params=processed_non_default_params,  # [IMPORTANT] - using processed_non_default_params ensures consistent params logged to langfuse for finetuning / eval datasets.
            litellm_params=litellm_params,
            custom_llm_provider=custom_llm_provider,
        )
        if mock_response or mock_tool_calls or mock_timeout:
            kwargs.pop("mock_timeout", None)  # remove for any fallbacks triggered
            return mock_completion(
                model,
                messages,
                stream=stream,
                n=n,
                mock_response=mock_response,
                mock_tool_calls=mock_tool_calls,
                logging=logging,
                acompletion=acompletion,
                mock_delay=kwargs.get("mock_delay", None),
                custom_llm_provider=custom_llm_provider,
                mock_timeout=mock_timeout,
                timeout=timeout,
            )

        ## RESPONSES API BRIDGE LOGIC ## - check if model has 'mode: responses' in litellm.model_cost map
        # Only run the second bridge check if the first one didn't already
        # detect responses mode (e.g. via the "responses/" prefix).  The second
        # check handles cases like gpt-5.4+ with tools+reasoning_effort or
        # reasoningSummary/reasoning_summary without tools (AI SDK) that the first
        # (early) check doesn't cover.
        _reasoning_summary_for_bridge = peek_reasoning_summary_aliases(optional_params)
        if responses_api_model_info.get("mode") != "responses":
            responses_api_model_info, model = responses_api_bridge_check(
                model=model,
                custom_llm_provider=custom_llm_provider,
                web_search_options=web_search_options,
                tools=tools,
                reasoning_effort=reasoning_effort,
                reasoning_summary=_reasoning_summary_for_bridge,
            )

        # Use base_model (the true underlying model) for Azure model-type
        # detection when the deployment name differs from the model name.
        _azure_detection_model = base_model or model

        if responses_api_model_info.get("mode") == "responses":
            from litellm.completion_extras import responses_api_bridge

            optional_params, rs_val = (
                strip_reasoning_summary_aliases_from_optional_params(optional_params)
            )

            if isinstance(reasoning_effort, dict) and "summary" in reasoning_effort:
                optional_params["reasoning_effort"] = reasoning_effort
            elif rs_val is not None:
                eff = optional_params.get("reasoning_effort", reasoning_effort)
                if isinstance(eff, dict):
                    optional_params["reasoning_effort"] = {**eff, "summary": rs_val}
                elif eff is not None:
                    optional_params["reasoning_effort"] = {
                        "effort": eff,
                        "summary": rs_val,
                    }
                else:
                    optional_params["reasoning_effort"] = {"summary": rs_val}

            return responses_api_bridge.completion(
                model=model,
                messages=messages,
                headers=headers,
                model_response=model_response,
                api_key=api_key,
                api_base=api_base,
                acompletion=acompletion,
                logging_obj=logging,
                optional_params=optional_params,
                litellm_params=litellm_params,
                timeout=timeout,  # type: ignore
                client=client,  # pass AsyncOpenAI, OpenAI client
                custom_llm_provider=custom_llm_provider,
                encoding=_get_encoding(),
                stream=stream,
            )
        elif (
            custom_llm_provider == "openai"
            and OpenAIGPT5Config.is_model_gpt_5_model(model)
        ) or (
            custom_llm_provider == "azure"
            and litellm.AzureOpenAIGPT5Config.is_model_gpt_5_model(
                _azure_detection_model
            )
        ):
            optional_params, _ = strip_reasoning_summary_aliases_from_optional_params(
                optional_params
            )

        if custom_llm_provider == "azure":
            # azure configs
            ## check dynamic params ##
            dynamic_params = False
            if client is not None and (
                isinstance(client, openai.AzureOpenAI)
                or isinstance(client, openai.AsyncAzureOpenAI)
            ):
                dynamic_params = _check_dynamic_azure_params(
                    azure_client_params={"api_version": api_version},
                    azure_client=client,
                )

            api_type = get_secret("AZURE_API_TYPE") or "azure"

            api_base = api_base or litellm.api_base or get_secret("AZURE_API_BASE")

            api_version = (
                api_version
                or litellm.api_version
                or get_secret_str("AZURE_API_VERSION")
                or litellm.AZURE_DEFAULT_API_VERSION
            )

            api_key = (
                api_key
                or litellm.api_key
                or litellm.azure_key
                or get_secret_str("AZURE_OPENAI_API_KEY")
                or get_secret_str("AZURE_API_KEY")
            )

            azure_ad_token = optional_params.get("extra_body", {}).pop(
                "azure_ad_token", None
            ) or get_secret_str("AZURE_AD_TOKEN")

            azure_ad_token_provider = litellm_params.get(
                "azure_ad_token_provider", None
            )

            headers = headers or litellm.headers

            if extra_headers is not None:
                optional_params["extra_headers"] = extra_headers
            if max_retries is not None:
                optional_params["max_retries"] = max_retries

            if litellm.AzureOpenAIO1Config().is_o_series_model(
                model=_azure_detection_model
            ):
                ## LOAD CONFIG - if set
                config = litellm.AzureOpenAIO1Config.get_config()
                for k, v in config.items():
                    if (
                        k not in optional_params
                    ):  # completion(top_k=3) > azure_config(top_k=3) <- allows for dynamic variables to be passed in
                        optional_params[k] = v

                response = azure_o1_chat_completions.completion(
                    model=model,
                    messages=messages,
                    headers=headers,
                    api_key=api_key,
                    api_base=api_base,
                    api_version=api_version,
                    dynamic_params=dynamic_params,
                    azure_ad_token=azure_ad_token,
                    model_response=model_response,
                    print_verbose=print_verbose,
                    optional_params=optional_params,
                    litellm_params=litellm_params,
                    logger_fn=logger_fn,
                    logging_obj=logging,
                    acompletion=acompletion,
                    timeout=timeout,  # type: ignore
                    client=client,  # pass AsyncAzureOpenAI, AzureOpenAI client
                    custom_llm_provider=custom_llm_provider,
                )
            else:
                ## LOAD CONFIG - if set
                config = litellm.AzureOpenAIConfig.get_config()
                for k, v in config.items():
                    if (
                        k not in optional_params
                    ):  # completion(top_k=3) > azure_config(top_k=3) <- allows for dynamic variables to be passed in
                        optional_params[k] = v

                ## COMPLETION CALL
                response = azure_chat_completions.completion(
                    model=model,
                    messages=messages,
                    headers=headers,
                    api_key=api_key,
                    api_base=api_base,
                    api_version=api_version,
                    api_type=api_type,
                    dynamic_params=dynamic_params,
                    azure_ad_token=azure_ad_token,
                    azure_ad_token_provider=azure_ad_token_provider,
                    model_response=model_response,
                    print_verbose=print_verbose,
                    optional_params=optional_params,
                    litellm_params=litellm_params,
                    logger_fn=logger_fn,
                    logging_obj=logging,
                    acompletion=acompletion,
                    timeout=timeout,  # type: ignore
                    client=client,  # pass AsyncAzureOpenAI, AzureOpenAI client
                )

            if optional_params.get("stream", False):
                ## LOGGING
                logging.post_call(
                    input=messages,
                    api_key=api_key,
                    original_response=response,
                    additional_args={
                        "headers": headers,
                        "api_version": api_version,
                        "api_base": api_base,
                    },
                )
        elif custom_llm_provider == "azure_text":
            # azure configs
            api_type = get_secret_str("AZURE_API_TYPE") or "azure"

            api_base = api_base or litellm.api_base or get_secret_str("AZURE_API_BASE")

            if api_base is None:
                raise ValueError(
                    "api_base is required for Azure OpenAI LLM provider. Either set it dynamically or set the AZURE_API_BASE environment variable."
                )

            api_version = (
                api_version
                or litellm.api_version
                or get_secret_str("AZURE_API_VERSION")
            )

            api_key = (
                api_key
                or litellm.api_key
                or litellm.azure_key
                or get_secret_str("AZURE_OPENAI_API_KEY")
                or get_secret_str("AZURE_API_KEY")
            )

            azure_ad_token = optional_params.get("extra_body", {}).pop(
                "azure_ad_token", None
            ) or get_secret_str("AZURE_AD_TOKEN")

            azure_ad_token_provider = litellm_params.get(
                "azure_ad_token_provider", None
            )

            headers = headers or litellm.headers

            if extra_headers is not None:
                optional_params["extra_headers"] = extra_headers

            ## LOAD CONFIG - if set
            config = litellm.AzureOpenAIConfig.get_config()
            for k, v in config.items():
                if (
                    k not in optional_params
                ):  # completion(top_k=3) > azure_config(top_k=3) <- allows for dynamic variables to be passed in
                    optional_params[k] = v

            ## COMPLETION CALL
            response = azure_text_completions.completion(
                model=model,
                messages=messages,
                headers=headers,
                api_key=api_key,
                api_base=api_base,
                api_version=cast(str, api_version),
                api_type=api_type,
                azure_ad_token=azure_ad_token,
                azure_ad_token_provider=azure_ad_token_provider,
                model_response=model_response,
                print_verbose=print_verbose,
                optional_params=optional_params,
                litellm_params=litellm_params,
                logger_fn=logger_fn,
                logging_obj=logging,
                acompletion=acompletion,
                timeout=timeout,
                client=client,  # pass AsyncAzureOpenAI, AzureOpenAI client
            )

            if optional_params.get("stream", False) or acompletion is True:
                ## LOGGING
                logging.post_call(
                    input=messages,
                    api_key=api_key,
                    original_response=response,
                    additional_args={
                        "headers": headers,
                        "api_version": api_version,
                        "api_base": api_base,
                    },
                )
        elif custom_llm_provider == "deepseek":
            ## COMPLETION CALL

            try:
                response = base_llm_http_handler.completion(
                    model=model,
                    messages=messages,
                    headers=headers,
                    model_response=model_response,
                    api_key=api_key,
                    api_base=api_base,
                    acompletion=acompletion,
                    logging_obj=logging,
                    optional_params=optional_params,
                    litellm_params=litellm_params,
                    shared_session=shared_session,
                    timeout=timeout,  # type: ignore
                    client=client,
                    custom_llm_provider=custom_llm_provider,
                    encoding=_get_encoding(),
                    stream=stream,
                    provider_config=provider_config,
                )
            except Exception as e:
                ## LOGGING - log the original exception returned
                logging.post_call(
                    input=messages,
                    api_key=api_key,
                    original_response=str(e),
                    additional_args={"headers": headers},
                )
                raise e

        elif custom_llm_provider == "azure_ai":
            from litellm.llms.azure_ai.common_utils import AzureFoundryModelInfo

            azure_ai_route = AzureFoundryModelInfo.get_azure_ai_route(model)

            # Check if this is an agents route - model format: azure_ai/agents/<agent_id>
            if azure_ai_route == "agents":
                from litellm.llms.azure_ai.agents import AzureAIAgentsConfig

                api_base = AzureFoundryModelInfo.get_api_base(api_base)
                if api_base is None:
                    raise ValueError(
                        "Azure AI Agents requests require an api_base. "
                        "Set `api_base` or the AZURE_AI_API_BASE env var."
                    )
                api_key = AzureFoundryModelInfo.get_api_key(api_key)

                response = AzureAIAgentsConfig.completion(
                    model=model,
                    messages=messages,
                    api_base=api_base,
                    api_key=api_key,
                    model_response=model_response,
                    logging_obj=logging,
                    optional_params=optional_params,
                    litellm_params=litellm_params,
                    timeout=timeout,
                    acompletion=acompletion,
                    stream=stream,
                    headers=headers or litellm.headers,
                )

            # Check if this is a Claude model - route to Azure Anthropic handler
            elif "claude" in model.lower():
                # Use Azure Anthropic handler for Claude models
                api_base = AzureFoundryModelInfo.get_api_base(api_base)
                if api_base is None:
                    raise ValueError(
                        "Azure Anthropic requests require an api_base. "
                        "Set `api_base` or the AZURE_AI_API_BASE env var."
                    )
                api_key = AzureFoundryModelInfo.get_api_key(api_key)

                # Ensure the URL ends with /v1/messages for Anthropic
                if api_base:
                    api_base = api_base.rstrip("/")
                    if not api_base.endswith("/v1/messages"):
                        if "/anthropic" in api_base:
                            parts = api_base.split("/anthropic", 1)
                            api_base = parts[0] + "/anthropic"
                        else:
                            api_base = api_base + "/anthropic"
                        api_base = api_base + "/v1/messages"

                response = azure_anthropic_chat_completions.completion(
                    model=model,
                    messages=messages,
                    api_base=api_base,
                    acompletion=acompletion,
                    custom_prompt_dict=litellm.custom_prompt_dict,
                    model_response=model_response,
                    print_verbose=print_verbose,
                    optional_params=optional_params,
                    litellm_params=litellm_params,
                    logger_fn=logger_fn,
                    encoding=_get_encoding(),
                    api_key=api_key,
                    logging_obj=logging,
                    headers=headers,
                    timeout=timeout,
                    client=client,
                    custom_llm_provider=custom_llm_provider,
                )
                if optional_params.get("stream", False) or acompletion is True:
                    ## LOGGING
                    logging.post_call(
                        input=messages,
                        api_key=api_key,
                        original_response=response,
                    )
                response = response
            else:
                # Non-Claude models use standard Azure AI flow
                api_base = AzureFoundryModelInfo.get_api_base(api_base)
                # set API KEY
                api_key = AzureFoundryModelInfo.get_api_key(api_key)

                headers = headers or litellm.headers

                if extra_headers is not None:
                    optional_params["extra_headers"] = extra_headers

                ## FOR COHERE
                if "command-r" in model:  # make sure tool call in messages are str
                    messages = stringify_json_tool_call_content(messages=messages)

                ## COMPLETION CALL
                try:
                    response = base_llm_http_handler.completion(
                        model=model,
                        messages=messages,
                        headers=headers,
                        model_response=model_response,
                        api_key=api_key,
                        api_base=api_base,
                        acompletion=acompletion,
                        logging_obj=logging,
                        optional_params=optional_params,
                        litellm_params=litellm_params,
                        shared_session=shared_session,
                        timeout=timeout,  # type: ignore
                        client=client,  # pass AsyncOpenAI, OpenAI client
                        custom_llm_provider=custom_llm_provider,
                        encoding=_get_encoding(),
                        stream=stream,
                    )
                except Exception as e:
                    ## LOGGING - log the original exception returned
                    logging.post_call(
                        input=messages,
                        api_key=api_key,
                        original_response=str(e),
                        additional_args={"headers": headers},
                    )
                    raise e

                if optional_params.get("stream", False):
                    ## LOGGING
                    logging.post_call(
                        input=messages,
                        api_key=api_key,
                        original_response=response,
                        additional_args={"headers": headers},
                    )
        elif (
            custom_llm_provider == "text-completion-openai"
            or "ft:babbage-002" in model
            or "ft:davinci-002" in model  # support for finetuned completion models
            or custom_llm_provider
            in litellm.openai_text_completion_compatible_providers
            and kwargs.get("text_completion") is True
        ):
            openai.api_type = "openai"

            api_base = (
                api_base
                or litellm.api_base
                or get_secret("OPENAI_BASE_URL")
                or get_secret("OPENAI_API_BASE")
                or "https://api.openai.com/v1"
            )

            openai.api_version = None
            # set API KEY

            api_key = (
                api_key
                or litellm.api_key
                or litellm.openai_key
                or get_secret("OPENAI_API_KEY")
            )

            headers = headers or litellm.headers

            ## LOAD CONFIG - if set
            config = litellm.OpenAITextCompletionConfig.get_config()
            for k, v in config.items():
                if (
                    k not in optional_params
                ):  # completion(top_k=3) > openai_text_config(top_k=3) <- allows for dynamic variables to be passed in
                    optional_params[k] = v
            if litellm.organization:
                openai.organization = litellm.organization

            if (
                len(messages) > 0
                and "content" in messages[0]
                and isinstance(messages[0]["content"], list)
            ):
                # text-davinci-003 can accept a string or array, if it's an array, assume the array is set in messages[0]['content']
                # https://platform.openai.com/docs/api-reference/completions/create
                prompt = messages[0]["content"]
            else:
                prompt = " ".join([message["content"] for message in messages])  # type: ignore

            ## COMPLETION CALL
            _response = openai_text_completions.completion(
                model=model,
                messages=messages,
                headers=headers,
                model_response=model_response,
                print_verbose=print_verbose,
                api_key=api_key,
                custom_llm_provider=custom_llm_provider,
                api_base=api_base,
                acompletion=acompletion,
                client=client,  # pass AsyncOpenAI, OpenAI client
                logging_obj=logging,
                optional_params=optional_params,
                litellm_params=litellm_params,
                logger_fn=logger_fn,
                timeout=timeout,  # type: ignore
            )

            if (
                optional_params.get("stream", False) is False
                and acompletion is False
                and text_completion is False
            ):
                # convert to chat completion response
                _response = litellm.OpenAITextCompletionConfig().convert_to_chat_model_response_object(
                    response_object=_response, model_response_object=model_response
                )

            if optional_params.get("stream", False) or acompletion is True:
                ## LOGGING
                logging.post_call(
                    input=messages,
                    api_key=api_key,
                    original_response=_response,
                    additional_args={"headers": headers},
                )
            response = _response
        elif custom_llm_provider == "fireworks_ai":
            ## COMPLETION CALL
            try:
                response = base_llm_http_handler.completion(
                    model=model,
                    messages=messages,
                    headers=headers,
                    model_response=model_response,
                    api_key=api_key,
                    api_base=api_base,
                    acompletion=acompletion,
                    logging_obj=logging,
                    optional_params=optional_params,
                    litellm_params=litellm_params,
                    shared_session=shared_session,
                    timeout=timeout,  # type: ignore
                    client=client,
                    custom_llm_provider=custom_llm_provider,
                    encoding=_get_encoding(),
                    stream=stream,
                    provider_config=provider_config,
                )
            except Exception as e:
                ## LOGGING - log the original exception returned
                logging.post_call(
                    input=messages,
                    api_key=api_key,
                    original_response=str(e),
                    additional_args={"headers": headers},
                )
                raise e
        elif custom_llm_provider == "heroku":
            try:
                response = base_llm_http_handler.completion(
                    model=model,
                    messages=messages,
                    headers=headers,
                    model_response=model_response,
                    api_key=api_key,
                    api_base=api_base,
                    acompletion=acompletion,
                    logging_obj=logging,
                    optional_params=optional_params,
                    litellm_params=litellm_params,
                    shared_session=shared_session,
                    timeout=timeout,
                    client=client,
                    custom_llm_provider=custom_llm_provider,
                    encoding=_get_encoding(),
                    stream=stream,
                    provider_config=provider_config,
                )
            except Exception as e:
                logging.post_call(
                    input=messages,
                    api_key=api_key,
                    original_response=str(e),
                    additional_args={"headers": headers},
                )
                raise e

        elif custom_llm_provider == "ragflow":
            ## COMPLETION CALL - RAGFlow uses HTTP handler to support custom URL paths
            try:
                response = base_llm_http_handler.completion(
                    model=model,
                    messages=messages,
                    headers=headers,
                    model_response=model_response,
                    api_key=api_key,
                    api_base=api_base,
                    acompletion=acompletion,
                    logging_obj=logging,
                    optional_params=optional_params,
                    litellm_params=litellm_params,
                    shared_session=shared_session,
                    timeout=timeout,
                    client=client,
                    custom_llm_provider=custom_llm_provider,
                    encoding=_get_encoding(),
                    stream=stream,
                    provider_config=provider_config,
                )
            except Exception as e:
                logging.post_call(
                    input=messages,
                    api_key=api_key,
                    original_response=str(e),
                    additional_args={"headers": headers},
                )
                raise e
        elif custom_llm_provider == "xai":
            ## COMPLETION CALL
            try:
                response = base_llm_http_handler.completion(
                    model=model,
                    messages=messages,
                    headers=headers,
                    model_response=model_response,
                    api_key=api_key,
                    api_base=api_base,
                    acompletion=acompletion,
                    logging_obj=logging,
                    optional_params=optional_params,
                    litellm_params=litellm_params,
                    shared_session=shared_session,
                    timeout=timeout,  # type: ignore
                    client=client,
                    custom_llm_provider=custom_llm_provider,
                    encoding=_get_encoding(),
                    stream=stream,
                    provider_config=provider_config,
                )
            except Exception as e:
                ## LOGGING - log the original exception returned
                logging.post_call(
                    input=messages,
                    api_key=api_key,
                    original_response=str(e),
                    additional_args={"headers": headers},
                )
                raise e
        elif custom_llm_provider == "groq":
            api_base = (
                api_base  # for deepinfra/perplexity/anyscale/groq/friendliai we check in get_llm_provider and pass in the api base from there
                or litellm.api_base
                or get_secret("GROQ_API_BASE")
                or "https://api.groq.com/openai/v1"
            )

            # set API KEY
            api_key = (
                api_key
                or litellm.api_key  # for deepinfra/perplexity/anyscale/friendliai we check in get_llm_provider and pass in the api key from there
                or litellm.groq_key
                or get_secret("GROQ_API_KEY")
            )

            headers = headers or litellm.headers

            ## LOAD CONFIG - if set
            config = litellm.GroqChatConfig.get_config()
            for k, v in config.items():
                if (
                    k not in optional_params
                ):  # completion(top_k=3) > openai_config(top_k=3) <- allows for dynamic variables to be passed in
                    optional_params[k] = v

            response = base_llm_http_handler.completion(
                model=model,
                stream=stream,
                messages=messages,
                acompletion=acompletion,
                api_base=api_base,
                model_response=model_response,
                optional_params=optional_params,
                litellm_params=litellm_params,
                shared_session=shared_session,
                custom_llm_provider=custom_llm_provider,
                timeout=timeout,
                headers=headers,
                encoding=_get_encoding(),
                api_key=api_key,
                logging_obj=logging,  # model call logging done inside the class as we make need to modify I/O to fit aleph alpha's requirements
                client=client,
            )
        elif custom_llm_provider == "bedrock_mantle":
            api_base = (
                api_base or litellm.api_base or get_secret("BEDROCK_MANTLE_API_BASE")
            )
            api_key = api_key or litellm.api_key or get_secret("BEDROCK_MANTLE_API_KEY")
            headers = headers or litellm.headers
            config = litellm.BedrockMantleChatConfig.get_config()
            for k, v in config.items():
                if k not in optional_params:
                    optional_params[k] = v
            response = base_llm_http_handler.completion(
                model=model,
                stream=stream,
                messages=messages,
                acompletion=acompletion,
                api_base=api_base,
                model_response=model_response,
                optional_params=optional_params,
                litellm_params=litellm_params,
                shared_session=shared_session,
                custom_llm_provider=custom_llm_provider,
                timeout=timeout,
                headers=headers,
                encoding=_get_encoding(),
                api_key=api_key,
                logging_obj=logging,
                client=client,
            )
        elif custom_llm_provider == "a2a":
            # A2A (Agent-to-Agent) Protocol
            # Resolve agent configuration from registry if model format is "a2a/<agent-name>"
            (
                api_base,
                api_key,
                headers,
            ) = litellm.A2AConfig.resolve_agent_config_from_registry(
                model=model,
                api_base=api_base,
                api_key=api_key,
                headers=headers,
                optional_params=optional_params,
            )

            # Fall back to environment variables and defaults
            api_base = api_base or litellm.api_base or get_secret_str("A2A_API_BASE")

            if api_base is None:
                raise Exception(
                    "api_base is required for A2A provider. "
                    "Either provide api_base parameter, set A2A_API_BASE environment variable, "
                    "or register the agent in the proxy with model='a2a/<agent-name>'."
                )

            headers = headers or litellm.headers

            response = base_llm_http_handler.completion(
                model=model,
                stream=stream,
                messages=messages,
                acompletion=acompletion,
                api_base=api_base,
                model_response=model_response,
                optional_params=optional_params,
                litellm_params=litellm_params,
                shared_session=shared_session,
                custom_llm_provider=custom_llm_provider,
                timeout=timeout,
                headers=headers,
                encoding=_get_encoding(),
                api_key=api_key,
                logging_obj=logging,
                client=client,
                provider_config=provider_config,
            )
        elif custom_llm_provider == "gigachat":
            # GigaChat - Sber AI's LLM (Russia)
            api_key = (
                api_key
                or litellm.api_key
                or litellm.gigachat_key
                or get_secret("GIGACHAT_API_KEY")
                or get_secret("GIGACHAT_CREDENTIALS")
            )

            headers = headers or litellm.headers or {}

            ## COMPLETION CALL
            try:
                response = base_llm_http_handler.completion(
                    model=model,
                    messages=messages,
                    headers=headers,
                    model_response=model_response,
                    api_key=api_key,
                    api_base=api_base,
                    acompletion=acompletion,
                    logging_obj=logging,
                    optional_params=optional_params,
                    litellm_params=litellm_params,
                    shared_session=shared_session,
                    timeout=timeout,
                    client=client,
                    custom_llm_provider=custom_llm_provider,
                    encoding=_get_encoding(),
                    stream=stream,
                    provider_config=provider_config,
                )
            except Exception as e:
                ## LOGGING - log the original exception returned
                logging.post_call(
                    input=messages,
                    api_key=api_key,
                    original_response=str(e),
                    additional_args={"headers": headers},
                )
                raise e

        elif custom_llm_provider == "sap":
            headers = headers or litellm.headers
            ## LOAD CONFIG - if set
            config = litellm.GenAIHubOrchestrationConfig.get_config()
            for k, v in config.items():
                if (
                    k not in optional_params
                ):  # completion(top_k=3) > openai_config(top_k=3) <- allows for dynamic variables to be passed in
                    optional_params[k] = v

            response = sap_gen_ai_hub_chat_completions.completion(
                model=model,
                messages=messages,
                headers=headers,
                model_response=model_response,
                acompletion=acompletion,
                logging_obj=logging,
                optional_params=optional_params,
                litellm_params=litellm_params,
                timeout=timeout,  # type: ignore
                shared_session=shared_session,
                client=client,
                custom_llm_provider=custom_llm_provider,
                encoding=_get_encoding(),
                api_key=api_key,
                api_base=api_base,
                stream=stream,
            )
        elif custom_llm_provider == "aiohttp_openai":
            # NEW aiohttp provider for 10-100x higher RPS
            api_base = (
                api_base  # for deepinfra/perplexity/anyscale/groq/friendliai we check in get_llm_provider and pass in the api base from there
                or litellm.api_base
                or get_secret("OPENAI_BASE_URL")
                or get_secret("OPENAI_API_BASE")
                or "https://api.openai.com/v1"
            )
            # set API KEY
            api_key = (
                api_key
                or litellm.api_key  # for deepinfra/perplexity/anyscale/friendliai we check in get_llm_provider and pass in the api key from there
                or litellm.openai_key
                or get_secret("OPENAI_API_KEY")
            )

            headers = headers or litellm.headers

            if extra_headers is not None:
                optional_params["extra_headers"] = extra_headers
            response = base_llm_aiohttp_handler.completion(
                model=model,
                messages=messages,
                headers=headers,
                model_response=model_response,
                api_key=api_key,
                api_base=api_base,
                acompletion=acompletion,
                logging_obj=logging,
                optional_params=optional_params,
                litellm_params=litellm_params,
                timeout=timeout,
                client=client,
                custom_llm_provider=custom_llm_provider,
                encoding=_get_encoding(),
                stream=stream,
            )
        elif custom_llm_provider == "cometapi":
            api_key = (
                api_key
                or litellm.cometapi_key
                or get_secret_str("COMETAPI_KEY")
                or litellm.api_key
            )

            api_base = (
                api_base
                or litellm.api_base
                or get_secret_str("COMETAPI_API_BASE")
                or "https://api.cometapi.com/v1"
            )

            ## COMPLETION CALL
            response = base_llm_http_handler.completion(
                model=model,
                messages=messages,
                headers=headers,
                model_response=model_response,
                api_key=api_key,
                api_base=api_base,
                acompletion=acompletion,
                logging_obj=logging,
                optional_params=optional_params,
                litellm_params=litellm_params,
                shared_session=shared_session,
                timeout=timeout,
                client=client,
                custom_llm_provider=custom_llm_provider,
                encoding=_get_encoding(),
                stream=stream,
                provider_config=provider_config,
            )

            ## LOGGING
            logging.post_call(
                input=messages, api_key=api_key, original_response=response
            )
        elif custom_llm_provider == "minimax":
            api_key = api_key or get_secret_str("MINIMAX_API_KEY") or litellm.api_key

            api_base = (
                api_base
                or litellm.api_base
                or get_secret_str("MINIMAX_API_BASE")
                or "https://api.minimax.io/v1"
            )

            response = base_llm_http_handler.completion(
                model=model,
                messages=messages,
                api_base=api_base,
                custom_llm_provider=custom_llm_provider,
                model_response=model_response,
                encoding=_get_encoding(),
                logging_obj=logging,
                optional_params=optional_params,
                timeout=timeout,
                litellm_params=litellm_params,
                shared_session=shared_session,
                acompletion=acompletion,
                stream=stream,
                api_key=api_key,
                headers=headers,
                client=client,
                provider_config=provider_config,
            )
            logging.post_call(
                input=messages, api_key=api_key, original_response=response
            )
        elif custom_llm_provider == "hosted_vllm":
            api_base = (
                api_base or litellm.api_base or get_secret_str("HOSTED_VLLM_API_BASE")
            )

            response = base_llm_http_handler.completion(
                model=model,
                messages=messages,
                api_base=api_base,
                custom_llm_provider=custom_llm_provider,
                model_response=model_response,
                encoding=_get_encoding(),
                logging_obj=logging,
                optional_params=optional_params,
                timeout=timeout,
                litellm_params=litellm_params,
                shared_session=shared_session,
                acompletion=acompletion,
                stream=stream,
                api_key=api_key,
                headers=headers,
                client=client,
                provider_config=provider_config,
            )
            logging.post_call(
                input=messages, api_key=api_key, original_response=response
            )
        elif (
            model in litellm.open_ai_chat_completion_models
            or custom_llm_provider == "custom_openai"
            or custom_llm_provider == "deepinfra"
            or custom_llm_provider == "perplexity"
            or custom_llm_provider == "nvidia_nim"
            or custom_llm_provider == "cerebras"
            or custom_llm_provider == "baseten"
            or custom_llm_provider == "sambanova"
            or custom_llm_provider == "volcengine"
            or custom_llm_provider == "anyscale"
            or custom_llm_provider == "openai"
            or custom_llm_provider == "together_ai"
            or custom_llm_provider == "nebius"
            or custom_llm_provider == "wandb"
            or custom_llm_provider == "clarifai"
            or custom_llm_provider in litellm.openai_compatible_providers
            or JSONProviderRegistry.exists(
                custom_llm_provider
            )  # JSON-configured providers
            or "ft:gpt-3.5-turbo" in model  # finetune gpt-3.5-turbo
        ):  # allow user to make an openai call with a custom base
            # note: if a user sets a custom base - we should ensure this works
            # allow for the setting of dynamic and stateful api-bases
            api_base = (
                api_base  # for deepinfra/perplexity/anyscale/groq/friendliai we check in get_llm_provider and pass in the api base from there
                or litellm.api_base
                or get_secret("OPENAI_BASE_URL")
                or get_secret("OPENAI_API_BASE")
                or "https://api.openai.com/v1"
            )
            organization = (
                organization
                or litellm.organization
                or get_secret("OPENAI_ORGANIZATION")
                or None  # default - https://github.com/openai/openai-python/blob/284c1799070c723c6a553337134148a7ab088dd8/openai/util.py#L105
            )
            openai.organization = organization
            # set API KEY
            api_key = (
                api_key
                or litellm.api_key  # for deepinfra/perplexity/anyscale/friendliai we check in get_llm_provider and pass in the api key from there
                or litellm.openai_key
                or get_secret("OPENAI_API_KEY")
            )

            headers = headers or litellm.headers

            # Add GitHub Copilot headers (same as /responses endpoint does)
            if custom_llm_provider == "github_copilot":
                from litellm.llms.github_copilot.authenticator import Authenticator
                from litellm.llms.github_copilot.common_utils import (
                    get_copilot_default_headers,
                )

                copilot_auth = Authenticator()
                copilot_api_key = copilot_auth.get_api_key()
                copilot_headers = get_copilot_default_headers(copilot_api_key)
                if extra_headers:
                    copilot_headers.update(extra_headers)
                extra_headers = copilot_headers

            if extra_headers is not None:
                optional_params["extra_headers"] = extra_headers

            if (
                litellm.enable_preview_features and metadata is not None
            ):  # [PREVIEW] allow metadata to be passed to OPENAI
                openai_metadata = get_requester_metadata(metadata)
                if openai_metadata is not None:
                    optional_params["metadata"] = openai_metadata

            ## LOAD CONFIG - if set
            config = litellm.OpenAIConfig.get_config()
            for k, v in config.items():
                if (
                    k not in optional_params
                ):  # completion(top_k=3) > openai_config(top_k=3) <- allows for dynamic variables to be passed in
                    optional_params[k] = v

            ## COMPLETION CALL
            use_base_llm_http_handler = get_secret_bool(
                "EXPERIMENTAL_OPENAI_BASE_LLM_HTTP_HANDLER"
            )

            try:
                if use_base_llm_http_handler:
                    response = base_llm_http_handler.completion(
                        model=model,
                        messages=messages,
                        api_base=api_base,
                        custom_llm_provider=custom_llm_provider,
                        model_response=model_response,
                        encoding=_get_encoding(),
                        logging_obj=logging,
                        optional_params=optional_params,
                        timeout=timeout,
                        litellm_params=litellm_params,
                        shared_session=shared_session,
                        acompletion=acompletion,
                        stream=stream,
                        api_key=api_key,
                        headers=headers,
                        client=client,
                        provider_config=provider_config,
                    )
                else:
                    response = openai_chat_completions.completion(
                        model=model,
                        messages=messages,
                        headers=headers,
                        model_response=model_response,
                        print_verbose=print_verbose,
                        api_key=api_key,
                        api_base=api_base,
                        acompletion=acompletion,
                        logging_obj=logging,
                        optional_params=optional_params,
                        litellm_params=litellm_params,
                        logger_fn=logger_fn,
                        timeout=timeout,  # type: ignore
                        custom_prompt_dict=custom_prompt_dict,
                        client=client,  # pass AsyncOpenAI, OpenAI client
                        organization=organization,
                        custom_llm_provider=custom_llm_provider,
                        shared_session=shared_session,
                    )
            except Exception as e:
                ## LOGGING - log the original exception returned
                logging.post_call(
                    input=messages,
                    api_key=api_key,
                    original_response=str(e),
                    additional_args={"headers": headers},
                )
                raise e

            if optional_params.get("stream", False):
                ## LOGGING
                logging.post_call(
                    input=messages,
                    api_key=api_key,
                    original_response=response,
                    additional_args={"headers": headers},
                )

        elif custom_llm_provider == "mistral":
            api_key = api_key or litellm.api_key or get_secret("MISTRAL_API_KEY")
            api_base = (
                api_base
                or litellm.api_base
                or get_secret("MISTRAL_API_BASE")
                or "https://api.mistral.ai/v1"
            )

            response = base_llm_http_handler.completion(
                model=model,
                messages=messages,
                api_base=api_base,
                custom_llm_provider=custom_llm_provider,
                model_response=model_response,
                encoding=_get_encoding(),
                logging_obj=logging,
                optional_params=optional_params,
                timeout=timeout,
                litellm_params=litellm_params,
                shared_session=shared_session,
                acompletion=acompletion,
                stream=stream,
                api_key=api_key,
                headers=headers,
                client=client,
                provider_config=provider_config,
            )
        elif (
            "replicate" in model
            or custom_llm_provider == "replicate"
            or model in litellm.replicate_models
        ):
            # Setting the relevant API KEY for replicate, replicate defaults to using os.environ.get("REPLICATE_API_TOKEN")
            replicate_key = (
                api_key
                or litellm.replicate_key
                or litellm.api_key
                or get_secret("REPLICATE_API_KEY")
                or get_secret("REPLICATE_API_TOKEN")
            )

            api_base = (
                api_base
                or litellm.api_base
                or get_secret("REPLICATE_API_BASE")
                or "https://api.replicate.com/v1"
            )

            custom_prompt_dict = custom_prompt_dict or litellm.custom_prompt_dict

            model_response = replicate_chat_completion(  # type: ignore
                model=model,
                messages=messages,
                api_base=api_base,
                model_response=model_response,
                print_verbose=print_verbose,
                optional_params=optional_params,
                litellm_params=litellm_params,
                logger_fn=logger_fn,
                encoding=_get_encoding(),  # for calculating input/output tokens
                api_key=replicate_key,
                logging_obj=logging,
                custom_prompt_dict=custom_prompt_dict,
                acompletion=acompletion,
                headers=headers,
            )

            if optional_params.get("stream", False) is True:
                ## LOGGING
                logging.post_call(
                    input=messages,
                    api_key=replicate_key,
                    original_response=model_response,
                )

            response = model_response
        elif (
            "clarifai" in model
            or custom_llm_provider == "clarifai"
            or model in litellm.clarifai_models
        ):
            pass  # Deprecated - handled in the openai compatible provider section above
        elif custom_llm_provider == "anthropic_text":
            api_key = (
                api_key
                or litellm.anthropic_key
                or litellm.api_key
                or os.environ.get("ANTHROPIC_API_KEY")
            )
            custom_prompt_dict = custom_prompt_dict or litellm.custom_prompt_dict
            api_base = (
                api_base
                or litellm.api_base
                or get_secret("ANTHROPIC_API_BASE")
                or get_secret("ANTHROPIC_BASE_URL")
                or "https://api.anthropic.com/v1/complete"
            )

            # Check if we should disable automatic URL suffix appending
            disable_url_suffix = get_secret_bool("LITELLM_ANTHROPIC_DISABLE_URL_SUFFIX")
            if (
                api_base is not None
                and not disable_url_suffix
                and not api_base.endswith("/v1/complete")
            ):
                api_base += "/v1/complete"
            elif disable_url_suffix:
                verbose_logger.debug(
                    "LITELLM_ANTHROPIC_DISABLE_URL_SUFFIX is set, skipping /v1/complete suffix"
                )

            response = base_llm_http_handler.completion(
                model=model,
                stream=stream,
                messages=messages,
                acompletion=acompletion,
                api_base=api_base,
                model_response=model_response,
                optional_params=optional_params,
                litellm_params=litellm_params,
                shared_session=shared_session,
                custom_llm_provider="anthropic_text",
                timeout=timeout,
                headers=headers,
                encoding=_get_encoding(),
                api_key=api_key,
                logging_obj=logging,  # model call logging done inside the class as we make need to modify I/O to fit aleph alpha's requirements
            )
        elif custom_llm_provider == "anthropic":
            api_key = (
                api_key
                or litellm.anthropic_key
                or litellm.api_key
                or os.environ.get("ANTHROPIC_API_KEY")
            )
            custom_prompt_dict = custom_prompt_dict or litellm.custom_prompt_dict
            # call /messages
            # default route for all anthropic models
            api_base = (
                api_base
                or litellm.api_base
                or get_secret("ANTHROPIC_API_BASE")
                or get_secret("ANTHROPIC_BASE_URL")
                or "https://api.anthropic.com/v1/messages"
            )

            # Check if we should disable automatic URL suffix appending
            disable_url_suffix = get_secret_bool("LITELLM_ANTHROPIC_DISABLE_URL_SUFFIX")
            if (
                api_base is not None
                and not disable_url_suffix
                and not api_base.endswith("/v1/messages")
            ):
                api_base += "/v1/messages"
            elif disable_url_suffix:
                verbose_logger.debug(
                    "LITELLM_ANTHROPIC_DISABLE_URL_SUFFIX is set, skipping /v1/messages suffix"
                )

            response = anthropic_chat_completions.completion(
                model=model,
                messages=messages,
                api_base=api_base,
                acompletion=acompletion,
                custom_prompt_dict=litellm.custom_prompt_dict,
                model_response=model_response,
                print_verbose=print_verbose,
                optional_params=optional_params,
                litellm_params=litellm_params,
                logger_fn=logger_fn,
                encoding=_get_encoding(),  # for calculating input/output tokens
                api_key=api_key,
                logging_obj=logging,
                headers=headers,
                timeout=timeout,
                client=client,
                custom_llm_provider=custom_llm_provider,
            )
            if optional_params.get("stream", False) or acompletion is True:
                ## LOGGING
                logging.post_call(
                    input=messages,
                    api_key=api_key,
                    original_response=response,
                )
            response = response
        elif custom_llm_provider == "nlp_cloud":
            nlp_cloud_key = (
                api_key
                or litellm.nlp_cloud_key
                or get_secret("NLP_CLOUD_API_KEY")
                or litellm.api_key
            )

            api_base = (
                api_base
                or litellm.api_base
                or get_secret("NLP_CLOUD_API_BASE")
                or "https://api.nlpcloud.io/v1/gpu/"
            )

            response = nlp_cloud_chat_completion(
                model=model,
                messages=messages,
                api_base=api_base,
                model_response=model_response,
                print_verbose=print_verbose,
                optional_params=optional_params,
                litellm_params=litellm_params,
                logger_fn=logger_fn,
                encoding=_get_encoding(),
                api_key=nlp_cloud_key,
                logging_obj=logging,
            )

            if "stream" in optional_params and optional_params["stream"] is True:
                # don't try to access stream object,
                response = CustomStreamWrapper(
                    response,
                    model,
                    custom_llm_provider="nlp_cloud",
                    logging_obj=logging,
                )

            if optional_params.get("stream", False) or acompletion is True:
                ## LOGGING
                logging.post_call(
                    input=messages,
                    api_key=api_key,
                    original_response=response,
                )

            response = response
        elif custom_llm_provider == "aleph_alpha":
            aleph_alpha_key = (
                api_key
                or litellm.aleph_alpha_key
                or get_secret("ALEPH_ALPHA_API_KEY")
                or get_secret("ALEPHALPHA_API_KEY")
                or litellm.api_key
            )

            api_base = (
                api_base
                or litellm.api_base
                or get_secret("ALEPH_ALPHA_API_BASE")
                or "https://api.aleph-alpha.com/complete"
            )

            model_response = aleph_alpha.completion(
                model=model,
                messages=messages,
                api_base=api_base,
                model_response=model_response,
                print_verbose=print_verbose,
                optional_params=optional_params,
                litellm_params=litellm_params,
                logger_fn=logger_fn,
                encoding=_get_encoding(),
                default_max_tokens_to_sample=litellm.max_tokens,
                api_key=aleph_alpha_key,
                logging_obj=logging,  # model call logging done inside the class as we make need to modify I/O to fit aleph alpha's requirements
            )

            if "stream" in optional_params and optional_params["stream"] is True:
                # don't try to access stream object,
                response = CustomStreamWrapper(
                    model_response,
                    model,
                    custom_llm_provider="aleph_alpha",
                    logging_obj=logging,
                )
                return response
            response = model_response
        elif custom_llm_provider == "cohere_chat" or custom_llm_provider == "cohere":
            cohere_key = (
                api_key
                or litellm.cohere_key
                or get_secret_str("COHERE_API_KEY")
                or get_secret_str("CO_API_KEY")
                or litellm.api_key
            )

            cohere_route = CohereModelInfo.get_cohere_route(model)
            verbose_logger.debug(f"Cohere route: {cohere_route}")
            # Set API base based on route
            if cohere_route == "v2":
                api_base = (
                    api_base
                    or litellm.api_base
                    or get_secret_str("COHERE_API_BASE")
                    or "https://api.cohere.com/v2/chat"
                )
                # Remove v2/ prefix from model name for the actual API call
                if "v2/" in model:
                    model = model.replace("v2/", "")
            else:
                api_base = (
                    api_base
                    or litellm.api_base
                    or get_secret_str("COHERE_API_BASE")
                    or "https://api.cohere.ai/v1/chat"
                )

            headers = headers or litellm.headers or {}
            if headers is None:
                headers = {}

            if extra_headers is not None:
                headers.update(extra_headers)

            verbose_logger.debug(f"Model: {model}, API Base: {api_base}")
            verbose_logger.debug(f"Provider Config: {provider_config}")
            response = base_llm_http_handler.completion(
                model=model,
                stream=stream,
                messages=messages,
                acompletion=acompletion,
                api_base=api_base,
                model_response=model_response,
                optional_params=optional_params,
                litellm_params=litellm_params,
                shared_session=shared_session,
                custom_llm_provider="cohere_chat",
                timeout=timeout,
                headers=headers,
                encoding=_get_encoding(),
                api_key=cohere_key,
                provider_config=provider_config,
                logging_obj=logging,  # model call logging done inside the class as we make need to modify I/O to fit aleph alpha's requirements
            )
        elif custom_llm_provider == "maritalk":
            maritalk_key = (
                api_key
                or litellm.maritalk_key
                or get_secret("MARITALK_API_KEY")
                or litellm.api_key
            )

            api_base = (
                api_base
                or litellm.api_base
                or get_secret("MARITALK_API_BASE")
                or "https://chat.maritaca.ai/api"
            )

            model_response = openai_like_chat_completion.completion(
                model=model,
                messages=messages,
                api_base=api_base,
                model_response=model_response,
                print_verbose=print_verbose,
                optional_params=optional_params,
                litellm_params=litellm_params,
                logger_fn=logger_fn,
                encoding=_get_encoding(),
                api_key=maritalk_key,
                logging_obj=logging,
                custom_llm_provider="maritalk",
                custom_prompt_dict=custom_prompt_dict,
            )

            response = model_response
        elif custom_llm_provider == "amazon_nova":
            api_key = (
                api_key
                or litellm.amazon_nova_api_key
                or get_secret_str("AMAZON_NOVA_API_KEY")
                or litellm.api_key
            )
            api_base = (
                api_base
                or litellm.api_base
                or get_secret_str("AMAZON_NOVA_API_BASE")
                or "https://api.nova.amazon.com/v1"
            )
            response = openai_like_chat_completion.completion(
                model=model,
                messages=messages,
                api_base=api_base,
                model_response=model_response,
                print_verbose=print_verbose,
                optional_params=optional_params,
                litellm_params=litellm_params,
                logger_fn=logger_fn,
                encoding=_get_encoding(),
                api_key=api_key,
                logging_obj=logging,
                timeout=timeout,
                custom_llm_provider=custom_llm_provider,
                custom_prompt_dict=custom_prompt_dict,
            )
        elif custom_llm_provider == "huggingface":
            huggingface_key = (
                api_key
                or litellm.huggingface_key
                or os.environ.get("HF_TOKEN")
                or os.environ.get("HUGGINGFACE_API_KEY")
                or litellm.api_key
            )
            hf_headers = headers or litellm.headers
            response = base_llm_http_handler.completion(
                model=model,
                messages=messages,
                headers=hf_headers,
                model_response=model_response,
                api_key=huggingface_key,
                api_base=api_base,
                acompletion=acompletion,
                logging_obj=logging,
                optional_params=optional_params,
                litellm_params=litellm_params,
                timeout=timeout,  # type: ignore
                client=client,
                custom_llm_provider=custom_llm_provider,
                encoding=_get_encoding(),
                stream=stream,
            )
        elif custom_llm_provider == "oci":
            response = base_llm_http_handler.completion(
                model=model,
                messages=messages,
                headers=headers,
                model_response=model_response,
                api_key=api_key,
                api_base=api_base,
                acompletion=acompletion,
                logging_obj=logging,
                optional_params=optional_params,
                litellm_params=litellm_params,
                timeout=timeout,  # type: ignore
                client=client,
                custom_llm_provider=custom_llm_provider,
                encoding=_get_encoding(),
                stream=stream,
            )
        elif custom_llm_provider == "compactifai":
            api_key = (
                api_key or get_secret_str("COMPACTIFAI_API_KEY") or litellm.api_key
            )

            api_base = api_base or "https://api.compactif.ai/v1"

            ## COMPLETION CALL
            response = base_llm_http_handler.completion(
                model=model,
                messages=messages,
                headers=headers,
                model_response=model_response,
                api_key=api_key,
                api_base=api_base,
                acompletion=acompletion,
                logging_obj=logging,
                optional_params=optional_params,
                litellm_params=litellm_params,
                timeout=timeout,
                client=client,
                custom_llm_provider=custom_llm_provider,
                encoding=_get_encoding(),
                stream=stream,
                provider_config=provider_config,
            )
        elif custom_llm_provider == "oobabooga":
            custom_llm_provider = "oobabooga"
            model_response = oobabooga.completion(
                model=model,
                messages=messages,
                model_response=model_response,
                api_base=api_base,  # type: ignore
                print_verbose=print_verbose,
                optional_params=optional_params,
                litellm_params=litellm_params,
                api_key=None,
                logger_fn=logger_fn,
                encoding=_get_encoding(),
                logging_obj=logging,
            )
            if "stream" in optional_params and optional_params["stream"] is True:
                # don't try to access stream object,
                response = CustomStreamWrapper(
                    model_response,
                    model,
                    custom_llm_provider="oobabooga",
                    logging_obj=logging,
                )
                return response
            response = model_response
        elif custom_llm_provider == "databricks":
            api_base = (
                api_base  # for databricks we check in get_llm_provider and pass in the api base from there
                or litellm.api_base
                or os.getenv("DATABRICKS_API_BASE")
            )

            # set API KEY
            api_key = (
                api_key
                or litellm.api_key  # for databricks we check in get_llm_provider and pass in the api key from there
                or litellm.databricks_key
                or get_secret("DATABRICKS_API_KEY")
            )

            headers = headers or litellm.headers

            ## COMPLETION CALL
            try:
                response = base_llm_http_handler.completion(
                    model=model,
                    stream=stream,
                    messages=messages,
                    acompletion=acompletion,
                    api_base=api_base,
                    model_response=model_response,
                    optional_params=optional_params,
                    litellm_params=litellm_params,
                    custom_llm_provider="databricks",
                    timeout=timeout,
                    headers=headers,
                    encoding=_get_encoding(),
                    api_key=api_key,
                    logging_obj=logging,  # model call logging done inside the class as we make need to modify I/O to fit aleph alpha's requirements
                    client=client,
                )
            except Exception as e:
                ## LOGGING - log the original exception returned
                logging.post_call(
                    input=messages,
                    api_key=api_key,
                    original_response=str(e),
                    additional_args={"headers": headers},
                )
                raise e

            if optional_params.get("stream", False):
                ## LOGGING
                logging.post_call(
                    input=messages,
                    api_key=api_key,
                    original_response=response,
                    additional_args={"headers": headers},
                )

        elif custom_llm_provider == "datarobot":
            response = base_llm_http_handler.completion(
                model=model,
                messages=messages,
                headers=headers,
                model_response=model_response,
                api_key=api_key,
                api_base=api_base,
                acompletion=acompletion,
                logging_obj=logging,
                optional_params=optional_params,
                litellm_params=litellm_params,
                timeout=timeout,  # type: ignore
                client=client,
                custom_llm_provider=custom_llm_provider,
                encoding=_get_encoding(),
                stream=stream,
                provider_config=provider_config,
            )
        elif custom_llm_provider == "openrouter":
            api_base = (
                api_base
                or litellm.api_base
                or get_secret_str("OPENROUTER_API_BASE")
                or "https://openrouter.ai/api/v1"
            )

            api_key = (
                api_key
                or litellm.api_key
                or litellm.openrouter_key
                or get_secret_str("OPENROUTER_API_KEY")
                or get_secret_str("OR_API_KEY")
            )

            openrouter_site_url = get_secret("OR_SITE_URL") or "https://litellm.ai"
            openrouter_app_name = get_secret("OR_APP_NAME") or "liteLLM"

            openrouter_headers = {
                "HTTP-Referer": openrouter_site_url,
                "X-Title": openrouter_app_name,
            }

            _headers = headers or litellm.headers
            if _headers:
                openrouter_headers.update(_headers)

            headers = openrouter_headers

            ## Load Config
            config = litellm.OpenrouterConfig.get_config()
            for k, v in config.items():
                if k == "extra_body":
                    # we use openai 'extra_body' to pass openrouter specific params - transforms, route, models
                    if "extra_body" in optional_params:
                        optional_params[k].update(v)
                    else:
                        optional_params[k] = v
                elif k not in optional_params:
                    optional_params[k] = v

            data = {"model": model, "messages": messages, **optional_params}

            ## COMPLETION CALL
            response = base_llm_http_handler.completion(
                model=model,
                stream=stream,
                messages=messages,
                acompletion=acompletion,
                api_base=api_base,
                model_response=model_response,
                optional_params=optional_params,
                litellm_params=litellm_params,
                shared_session=shared_session,
                custom_llm_provider="openrouter",
                timeout=timeout,
                headers=headers,
                encoding=_get_encoding(),
                api_key=api_key,
                logging_obj=logging,  # model call logging done inside the class as we make need to modify I/O to fit aleph alpha's requirements
                client=client,
            )
            ## LOGGING
            logging.post_call(
                input=messages, api_key=openai.api_key, original_response=response
            )
        elif custom_llm_provider == "vercel_ai_gateway":
            api_base = (
                api_base
                or litellm.api_base
                or get_secret_str("VERCEL_AI_GATEWAY_API_BASE")
                or "https://ai-gateway.vercel.sh/v1"
            )

            api_key = (
                api_key or litellm.api_key or get_secret("VERCEL_AI_GATEWAY_API_KEY")
            )

            vercel_site_url = get_secret("VERCEL_SITE_URL") or "https://litellm.ai"
            vercel_app_name = get_secret("VERCEL_APP_NAME") or "liteLLM"

            vercel_headers = {
                "http-referer": vercel_site_url,
                "x-title": vercel_app_name,
            }

            _headers = headers or litellm.headers
            if _headers:
                vercel_headers.update(_headers)

            headers = vercel_headers

            ## Load Config
            config = litellm.VercelAIGatewayConfig.get_config()
            for k, v in config.items():
                if k == "extra_body":
                    # we use openai 'extra_body' to pass vercel specific params - providerOptions
                    if "extra_body" in optional_params:
                        optional_params[k].update(v)
                    else:
                        optional_params[k] = v
                elif k not in optional_params:
                    optional_params[k] = v

            data = {"model": model, "messages": messages, **optional_params}

            ## COMPLETION CALL
            response = base_llm_http_handler.completion(
                model=model,
                stream=stream,
                messages=messages,
                acompletion=acompletion,
                api_base=api_base,
                model_response=model_response,
                optional_params=optional_params,
                litellm_params=litellm_params,
                shared_session=shared_session,
                custom_llm_provider="vercel_ai_gateway",
                timeout=timeout,
                headers=headers,
                encoding=_get_encoding(),
                api_key=api_key,
                logging_obj=logging,  # model call logging done inside the class as we make need to modify I/O to fit aleph alpha's requirements
                client=client,
            )
            ## LOGGING
            logging.post_call(
                input=messages, api_key=openai.api_key, original_response=response
            )
        elif (
            custom_llm_provider == "together_ai"
            or ("togethercomputer" in model)
            or (model in litellm.together_ai_models)
        ):
            """
            Deprecated. We now do together ai calls via the openai client - https://docs.together.ai/docs/openai-api-compatibility
            """
            pass
        elif custom_llm_provider == "palm":
            raise ValueError(
                "Palm was decommisioned on October 2024. Please use the `gemini/` route for Gemini Google AI Studio Models. Announcement: https://ai.google.dev/palm_docs/palm?hl=en"
            )
        elif custom_llm_provider == "vertex_ai_beta" or custom_llm_provider == "gemini":
            vertex_ai_project = (
                optional_params.pop("vertex_project", None)
                or optional_params.pop("vertex_ai_project", None)
                or litellm.vertex_project
                or get_secret("VERTEXAI_PROJECT")
            )
            vertex_ai_location = (
                optional_params.pop("vertex_location", None)
                or optional_params.pop("vertex_ai_location", None)
                or litellm.vertex_location
                or get_secret("VERTEXAI_LOCATION")
            )
            vertex_credentials = (
                optional_params.pop("vertex_credentials", None)
                or optional_params.pop("vertex_ai_credentials", None)
                or get_secret("VERTEXAI_CREDENTIALS")
            )

            gemini_api_key = (
                api_key
                or get_api_key_from_env()
                or get_secret("PALM_API_KEY")  # older palm api key should also work
                or litellm.api_key
            )

            api_base = api_base or litellm.api_base or get_secret("GEMINI_API_BASE")
            new_params = safe_deep_copy(optional_params or {})
            response = vertex_chat_completion.completion(  # type: ignore
                model=model,
                messages=messages,
                model_response=model_response,
                print_verbose=print_verbose,
                optional_params=new_params,
                litellm_params=litellm_params,  # type: ignore
                logger_fn=logger_fn,
                encoding=_get_encoding(),
                vertex_location=vertex_ai_location,
                vertex_project=vertex_ai_project,
                vertex_credentials=vertex_credentials,
                gemini_api_key=gemini_api_key,
                logging_obj=logging,
                acompletion=acompletion,
                timeout=timeout,
                custom_llm_provider=custom_llm_provider,  # type: ignore
                client=client,
                api_base=api_base,
                extra_headers=headers,
            )

        elif custom_llm_provider == "vertex_ai":
            vertex_ai_project = (
                optional_params.pop("vertex_project", None)
                or optional_params.pop("vertex_ai_project", None)
                or litellm.vertex_project
                or get_secret("VERTEXAI_PROJECT")
            )
            vertex_ai_location = (
                optional_params.pop("vertex_location", None)
                or optional_params.pop("vertex_ai_location", None)
                or litellm.vertex_location
                or get_secret("VERTEXAI_LOCATION")
            )
            vertex_credentials = (
                optional_params.pop("vertex_credentials", None)
                or optional_params.pop("vertex_ai_credentials", None)
                or get_secret("VERTEXAI_CREDENTIALS")
            )

            api_base = api_base or litellm.api_base or get_secret("VERTEXAI_API_BASE")

            new_params = safe_deep_copy(optional_params or {})
            model_route = get_vertex_ai_model_route(
                model=model, litellm_params=litellm_params
            )

            if model_route == VertexAIModelRoute.PARTNER_MODELS:
                model_response = vertex_partner_models_chat_completion.completion(
                    model=model,
                    messages=messages,
                    model_response=model_response,
                    print_verbose=print_verbose,
                    optional_params=new_params,
                    litellm_params=litellm_params,  # type: ignore
                    logger_fn=logger_fn,
                    encoding=_get_encoding(),
                    api_base=api_base,
                    vertex_location=vertex_ai_location,
                    vertex_project=vertex_ai_project,
                    vertex_credentials=vertex_credentials,
                    logging_obj=logging,
                    acompletion=acompletion,
                    headers=headers,
                    custom_prompt_dict=custom_prompt_dict,
                    timeout=timeout,
                    client=client,
                )
            elif model_route == VertexAIModelRoute.GEMINI:
                model_response = vertex_chat_completion.completion(  # type: ignore
                    model=model,
                    messages=messages,
                    model_response=model_response,
                    print_verbose=print_verbose,
                    optional_params=new_params,
                    litellm_params=litellm_params,  # type: ignore
                    logger_fn=logger_fn,
                    encoding=_get_encoding(),
                    vertex_location=vertex_ai_location,
                    vertex_project=vertex_ai_project,
                    vertex_credentials=vertex_credentials,
                    gemini_api_key=None,
                    logging_obj=logging,
                    acompletion=acompletion,
                    timeout=timeout,
                    custom_llm_provider=custom_llm_provider,  # type: ignore
                    client=client,
                    api_base=api_base,
                    extra_headers=headers,
                )
            elif model_route == VertexAIModelRoute.GEMMA:
                # Vertex Gemma Models with custom prediction endpoint
                model_response = vertex_gemma_chat_completion.completion(
                    model=model,
                    messages=messages,
                    model_response=model_response,
                    print_verbose=print_verbose,
                    optional_params=new_params,
                    litellm_params=litellm_params,  # type: ignore
                    logger_fn=logger_fn,
                    encoding=_get_encoding(),
                    api_base=api_base,
                    vertex_location=vertex_ai_location,
                    vertex_project=vertex_ai_project,
                    vertex_credentials=vertex_credentials,
                    logging_obj=logging,
                    acompletion=acompletion,
                    headers=headers,
                    custom_prompt_dict=custom_prompt_dict,
                    timeout=timeout,
                    client=client,
                )
            elif model_route == VertexAIModelRoute.MODEL_GARDEN:
                # Vertex Model Garden - OpenAI compatible models
                model_response = vertex_model_garden_chat_completion.completion(
                    model=model,
                    messages=messages,
                    model_response=model_response,
                    print_verbose=print_verbose,
                    optional_params=new_params,
                    litellm_params=litellm_params,  # type: ignore
                    logger_fn=logger_fn,
                    encoding=_get_encoding(),
                    api_base=api_base,
                    vertex_location=vertex_ai_location,
                    vertex_project=vertex_ai_project,
                    vertex_credentials=vertex_credentials,
                    logging_obj=logging,
                    acompletion=acompletion,
                    headers=headers,
                    custom_prompt_dict=custom_prompt_dict,
                    timeout=timeout,
                    client=client,
                )
            elif model_route == VertexAIModelRoute.AGENT_ENGINE:
                # Vertex AI Agent Engine (Reasoning Engines)
                from litellm.llms.vertex_ai.agent_engine.transformation import (
                    VertexAgentEngineConfig,
                )

                vertex_agent_engine_config = VertexAgentEngineConfig()

                # Update litellm_params with vertex credentials
                litellm_params["vertex_project"] = vertex_ai_project
                litellm_params["vertex_location"] = vertex_ai_location
                litellm_params["vertex_credentials"] = vertex_credentials

                model_response = base_llm_http_handler.completion(
                    model=model,
                    stream=stream,
                    messages=messages,
                    model_response=model_response,
                    optional_params=new_params,
                    litellm_params=litellm_params,  # type: ignore
                    encoding=_get_encoding(),
                    api_key=None,
                    api_base=api_base,
                    logging_obj=logging,
                    acompletion=acompletion,
                    timeout=timeout,
                    client=client,
                    custom_llm_provider="vertex_ai",
                    provider_config=vertex_agent_engine_config,
                    headers=headers or {},
                )
            else:  # VertexAIModelRoute.NON_GEMINI
                model_response = vertex_ai_non_gemini.completion(
                    model=model,
                    messages=messages,
                    model_response=model_response,
                    print_verbose=print_verbose,
                    optional_params=new_params,
                    litellm_params=litellm_params,
                    logger_fn=logger_fn,
                    encoding=_get_encoding(),
                    vertex_location=vertex_ai_location,
                    vertex_project=vertex_ai_project,
                    vertex_credentials=vertex_credentials,
                    logging_obj=logging,
                    acompletion=acompletion,
                )

                if (
                    "stream" in optional_params
                    and optional_params["stream"] is True
                    and acompletion is False
                ):
                    response = CustomStreamWrapper(
                        model_response,
                        model,
                        custom_llm_provider="vertex_ai",
                        logging_obj=logging,
                    )
                    return response
            response = model_response
        elif custom_llm_provider == "predibase":
            tenant_id = (
                optional_params.pop("tenant_id", None)
                or optional_params.pop("predibase_tenant_id", None)
                or litellm.predibase_tenant_id
                or get_secret("PREDIBASE_TENANT_ID")
            )

            if tenant_id is None:
                raise ValueError(
                    "Missing Predibase Tenant ID - Required for making the request. Set dynamically (e.g. `completion(..tenant_id=<MY-ID>)`) or in env - `PREDIBASE_TENANT_ID`."
                )

            api_base = (
                api_base
                or optional_params.pop("api_base", None)
                or optional_params.pop("base_url", None)
                or litellm.api_base
                or get_secret("PREDIBASE_API_BASE")
            )

            api_key = (
                api_key
                or litellm.api_key
                or litellm.predibase_key
                or get_secret("PREDIBASE_API_KEY")
            )

            _model_response = predibase_chat_completions.completion(
                model=model,
                messages=messages,
                model_response=model_response,
                print_verbose=print_verbose,
                optional_params=optional_params,
                litellm_params=litellm_params,
                logger_fn=logger_fn,
                encoding=_get_encoding(),
                logging_obj=logging,
                acompletion=acompletion,
                api_base=api_base,
                custom_prompt_dict=custom_prompt_dict,
                api_key=api_key,
                tenant_id=tenant_id,
                timeout=timeout,
            )

            if (
                "stream" in optional_params
                and optional_params["stream"] is True
                and acompletion is False
            ):
                return _model_response
            response = _model_response
        elif custom_llm_provider == "text-completion-codestral":
            api_base = (
                api_base
                or optional_params.pop("api_base", None)
                or optional_params.pop("base_url", None)
                or litellm.api_base
                or "https://codestral.mistral.ai/v1/fim/completions"
            )

            api_key = api_key or litellm.api_key or get_secret("CODESTRAL_API_KEY")

            text_completion_model_response = litellm.TextCompletionResponse(
                stream=stream
            )

            _model_response = codestral_text_completions.completion(  # type: ignore
                model=model,
                messages=messages,
                model_response=text_completion_model_response,
                print_verbose=print_verbose,
                optional_params=optional_params,
                litellm_params=litellm_params,
                logger_fn=logger_fn,
                encoding=_get_encoding(),
                logging_obj=logging,
                acompletion=acompletion,
                api_base=api_base,
                custom_prompt_dict=custom_prompt_dict,
                api_key=api_key,
                timeout=timeout,
            )

            if (
                "stream" in optional_params
                and optional_params["stream"] is True
                and acompletion is False
            ):
                return _model_response
            response = _model_response
        elif custom_llm_provider == "text-completion-inception":
            passed_api_base = (
                api_base
                or optional_params.pop("api_base", None)
                or optional_params.pop("base_url", None)
            )
            api_base = (
                passed_api_base
                or get_secret_str("INCEPTION_API_BASE")
                or "https://api.inceptionlabs.ai/v1"
            )
            # FIM is served at `/v1/fim/completions`; the OpenAI client appends
            # `/completions`, so point it at the `/v1/fim` base.
            api_base = api_base.rstrip("/")
            if not api_base.endswith("/fim"):
                api_base += "/fim"

            # Don't forward the server-managed Inception key to a caller-supplied
            # api_base; only resolve it for the default/server base, or when the
            # caller passes their own key.
            if passed_api_base is None or api_key:
                api_key = (
                    api_key
                    or litellm.inception_key
                    or get_secret_str("INCEPTION_API_KEY")
                )

            _response = openai_text_completions.completion(
                model=model,
                messages=messages,
                model_response=model_response,
                print_verbose=print_verbose,
                api_key=api_key,  # type: ignore[arg-type]
                custom_llm_provider="text-completion-inception",
                api_base=api_base,
                acompletion=acompletion,
                client=client,
                logging_obj=logging,
                optional_params=optional_params,
                litellm_params=litellm_params,
                logger_fn=logger_fn,
                timeout=timeout,  # type: ignore
            )

            if (
                optional_params.get("stream", False) is False
                and acompletion is False
                and text_completion is False
            ):
                _response = litellm.OpenAITextCompletionConfig().convert_to_chat_model_response_object(
                    response_object=_response, model_response_object=model_response
                )

            if optional_params.get("stream", False) or acompletion is True:
                logging.post_call(
                    input=messages,
                    api_key=api_key,
                    original_response=_response,
                    additional_args={"headers": headers},
                )
            response = _response
        elif custom_llm_provider in ("sagemaker_chat", "sagemaker_nova"):
            # boto3 reads keys from .env
            # sagemaker_chat: HF Messages API endpoints
            # sagemaker_nova: Nova models on SageMaker (OpenAI-compatible)
            model_response = base_llm_http_handler.completion(
                model=model,
                stream=stream,
                messages=messages,
                acompletion=acompletion,
                api_base=api_base,
                model_response=model_response,
                optional_params=optional_params,
                litellm_params=litellm_params,
                custom_llm_provider=custom_llm_provider,
                timeout=timeout,
                headers=headers,
                encoding=_get_encoding(),
                api_key=api_key,
                logging_obj=logging,  # model call logging done inside the class as we make need to modify I/O to fit aleph alpha's requirements
                client=client,
            )

            ## RESPONSE OBJECT
            response = model_response
        elif custom_llm_provider == "sagemaker":
            # boto3 reads keys from .env
            model_response = sagemaker_llm.completion(
                model=model,
                messages=messages,
                model_response=model_response,
                print_verbose=print_verbose,
                optional_params=optional_params,
                litellm_params=litellm_params,
                custom_prompt_dict=custom_prompt_dict,
                hf_model_name=hf_model_name,
                logger_fn=logger_fn,
                encoding=_get_encoding(),
                logging_obj=logging,
                acompletion=acompletion,
            )

            ## RESPONSE OBJECT
            response = model_response
        elif custom_llm_provider == "bedrock":
            # boto3 reads keys from .env
            custom_prompt_dict = custom_prompt_dict or litellm.custom_prompt_dict

            if "aws_bedrock_client" in optional_params:
                verbose_logger.warning(
                    "'aws_bedrock_client' is a deprecated param. Please move to another auth method - https://docs.litellm.ai/docs/providers/bedrock#boto3---authentication."
                )
                # Extract credentials for legacy boto3 client and pass thru to httpx
                aws_bedrock_client = optional_params.pop("aws_bedrock_client")
                creds = aws_bedrock_client._get_credentials().get_frozen_credentials()

                if creds.access_key:
                    optional_params["aws_access_key_id"] = creds.access_key
                if creds.secret_key:
                    optional_params["aws_secret_access_key"] = creds.secret_key
                if creds.token:
                    optional_params["aws_session_token"] = creds.token
                if (
                    "aws_region_name" not in optional_params
                    or optional_params["aws_region_name"] is None
                ):
                    optional_params["aws_region_name"] = (
                        aws_bedrock_client.meta.region_name
                    )

            bedrock_route = BedrockModelInfo.get_bedrock_route(model)
            if bedrock_route == "claude_platform":
                provider_config = ProviderConfigManager.get_provider_chat_config(
                    model=model,
                    provider=LlmProviders.BEDROCK,
                )
                model = BedrockModelInfo.get_claude_platform_model(model)
                response = base_llm_http_handler.completion(
                    model=model,
                    stream=stream,
                    messages=messages,
                    acompletion=acompletion,
                    api_base=api_base,
                    model_response=model_response,
                    optional_params=optional_params,
                    litellm_params=litellm_params,
                    shared_session=shared_session,
                    custom_llm_provider="bedrock",
                    timeout=timeout,
                    headers=headers,
                    encoding=_get_encoding(),
                    api_key=api_key,
                    logging_obj=logging,
                    client=client,
                    provider_config=provider_config,
                )
                return response
            elif bedrock_route == "converse":
                model = model.replace("converse/", "")
                response = bedrock_converse_chat_completion.completion(
                    model=model,
                    messages=messages,
                    custom_prompt_dict=custom_prompt_dict,
                    model_response=model_response,
                    optional_params=optional_params,
                    litellm_params=litellm_params,  # type: ignore
                    logger_fn=logger_fn,
                    encoding=_get_encoding(),
                    logging_obj=logging,
                    extra_headers=headers,  # Use merged headers instead of original extra_headers
                    timeout=timeout,
                    acompletion=acompletion,
                    client=client,
                    api_base=api_base,
                    api_key=api_key,
                )
            elif bedrock_route == "converse_like":
                model = model.replace("converse_like/", "")
                response = base_llm_http_handler.completion(
                    model=model,
                    stream=stream,
                    messages=messages,
                    acompletion=acompletion,
                    api_base=api_base,
                    model_response=model_response,
                    optional_params=optional_params,
                    litellm_params=litellm_params,
                    custom_llm_provider="bedrock",
                    timeout=timeout,
                    headers=headers,
                    encoding=_get_encoding(),
                    api_key=api_key,
                    logging_obj=logging,  # model call logging done inside the class as we make need to modify I/O to fit aleph alpha's requirements
                    client=client,
                )
            else:
                response = base_llm_http_handler.completion(
                    model=model,
                    stream=stream,
                    messages=messages,
                    acompletion=acompletion,
                    api_base=api_base,
                    model_response=model_response,
                    optional_params=optional_params,
                    litellm_params=litellm_params,
                    custom_llm_provider="bedrock",
                    timeout=timeout,
                    headers=headers,
                    encoding=_get_encoding(),
                    api_key=api_key,
                    logging_obj=logging,
                    client=client,
                )
        elif custom_llm_provider == "watsonx":
            response = watsonx_chat_completion.completion(
                model=model,
                messages=messages,
                headers=headers,
                model_response=model_response,
                print_verbose=print_verbose,
                api_key=api_key,
                api_base=api_base,
                acompletion=acompletion,
                logging_obj=logging,
                optional_params=optional_params,
                litellm_params=litellm_params,
                logger_fn=logger_fn,
                timeout=timeout,  # type: ignore
                custom_prompt_dict=custom_prompt_dict,
                client=client,  # pass AsyncOpenAI, OpenAI client
                encoding=_get_encoding(),
                custom_llm_provider="watsonx",
            )
        elif custom_llm_provider == "watsonx_text":
            api_key = (
                api_key
                or optional_params.pop("apikey", None)
                or get_secret_str("WATSONX_APIKEY")
                or get_secret_str("WATSONX_API_KEY")
                or get_secret_str("WX_API_KEY")
            )

            api_base = (
                api_base
                or optional_params.pop(
                    "url",
                    optional_params.pop(
                        "api_base", optional_params.pop("base_url", None)
                    ),
                )
                or get_secret_str("WATSONX_API_BASE")
                or get_secret_str("WATSONX_URL")
                or get_secret_str("WX_URL")
                or get_secret_str("WML_URL")
            )

            wx_credentials = optional_params.pop(
                "wx_credentials",
                optional_params.pop(
                    "watsonx_credentials", None
                ),  # follow {provider}_credentials, same as vertex ai
            )

            token: Optional[str] = None
            if wx_credentials is not None:
                api_base = wx_credentials.get("url", api_base)
                api_key = wx_credentials.get(
                    "apikey", wx_credentials.get("api_key", api_key)
                )
                token = wx_credentials.get(
                    "token",
                    wx_credentials.get(
                        "watsonx_token", None
                    ),  # follow format of {provider}_token, same as azure - e.g. 'azure_ad_token=..'
                )

            if token is not None:
                optional_params["token"] = token

            response = base_llm_http_handler.completion(
                model=model,
                stream=stream,
                messages=messages,
                acompletion=acompletion,
                api_base=api_base,
                model_response=model_response,
                optional_params=optional_params,
                litellm_params=litellm_params,
                shared_session=shared_session,
                custom_llm_provider="watsonx_text",
                timeout=timeout,
                headers=headers,
                encoding=_get_encoding(),
                api_key=api_key,
                logging_obj=logging,  # model call logging done inside the class as we make need to modify I/O to fit aleph alpha's requirements
                client=client,
            )
        elif custom_llm_provider == "vllm":
            custom_prompt_dict = custom_prompt_dict or litellm.custom_prompt_dict
            model_response = vllm_handler.completion(
                model=model,
                messages=messages,
                custom_prompt_dict=custom_prompt_dict,
                model_response=model_response,
                print_verbose=print_verbose,
                optional_params=optional_params,
                litellm_params=litellm_params,
                logger_fn=logger_fn,
                encoding=_get_encoding(),
                logging_obj=logging,
            )

            if (
                "stream" in optional_params and optional_params["stream"] is True
            ):  ## [BETA]
                # don't try to access stream object,
                response = CustomStreamWrapper(
                    model_response,
                    model,
                    custom_llm_provider="vllm",
                    logging_obj=logging,
                )
                return response

            ## RESPONSE OBJECT
            response = model_response
        elif custom_llm_provider == "ollama":
            api_base = (
                litellm.api_base
                or api_base
                or get_secret("OLLAMA_API_BASE")
                or "http://localhost:11434"
            )
            if api_key is not None and "Authorization" not in headers:
                headers["Authorization"] = f"Bearer {api_key}"

            response = base_llm_http_handler.completion(
                model=model,
                stream=stream,
                messages=messages,
                acompletion=acompletion,
                api_base=api_base,
                model_response=model_response,
                optional_params=optional_params,
                litellm_params=litellm_params,
                shared_session=shared_session,
                custom_llm_provider="ollama",
                timeout=timeout,
                headers=headers,
                encoding=_get_encoding(),
                api_key=api_key,
                logging_obj=logging,  # model call logging done inside the class as we make need to modify I/O to fit aleph alpha's requirements
                client=client,
            )

        elif custom_llm_provider == "ollama_chat":
            api_base = (
                litellm.api_base
                or api_base
                or get_secret("OLLAMA_API_BASE")
                or "http://localhost:11434"
            )

            api_key = (
                api_key
                or litellm.ollama_key
                or os.environ.get("OLLAMA_API_KEY")
                or litellm.api_key
            )
            if api_key is not None and "Authorization" not in headers:
                headers["Authorization"] = f"Bearer {api_key}"

            response = base_llm_http_handler.completion(
                model=model,
                stream=stream,
                messages=messages,
                acompletion=acompletion,
                api_base=api_base,
                model_response=model_response,
                optional_params=optional_params,
                litellm_params=litellm_params,
                shared_session=shared_session,
                custom_llm_provider="ollama_chat",
                timeout=timeout,
                headers=headers,
                encoding=_get_encoding(),
                api_key=api_key,
                logging_obj=logging,  # model call logging done inside the class as we make need to modify I/O to fit aleph alpha's requirements
                client=client,
            )

        elif custom_llm_provider == "triton":
            api_base = litellm.api_base or api_base
            response = base_llm_http_handler.completion(
                model=model,
                stream=stream,
                messages=messages,
                acompletion=acompletion,
                api_base=api_base,
                model_response=model_response,
                optional_params=optional_params,
                litellm_params=litellm_params,
                shared_session=shared_session,
                custom_llm_provider=custom_llm_provider,
                timeout=timeout,
                headers=headers,
                encoding=_get_encoding(),
                api_key=api_key,
                logging_obj=logging,
            )
        elif custom_llm_provider == "cloudflare":
            api_key = (
                api_key
                or litellm.cloudflare_api_key
                or litellm.api_key
                or get_secret("CLOUDFLARE_API_KEY")
            )
            account_id = get_secret("CLOUDFLARE_ACCOUNT_ID")
            api_base = (
                api_base
                or litellm.api_base
                or get_secret("CLOUDFLARE_API_BASE")
                or f"https://api.cloudflare.com/client/v4/accounts/{account_id}/ai/run/"
            )

            custom_prompt_dict = custom_prompt_dict or litellm.custom_prompt_dict
            response = base_llm_http_handler.completion(
                model=model,
                stream=stream,
                messages=messages,
                acompletion=acompletion,
                api_base=api_base,
                model_response=model_response,
                optional_params=optional_params,
                litellm_params=litellm_params,
                shared_session=shared_session,
                custom_llm_provider="cloudflare",
                timeout=timeout,
                headers=headers,
                encoding=_get_encoding(),
                api_key=api_key,
                logging_obj=logging,  # model call logging done inside the class as we make need to modify I/O to fit aleph alpha's requirements
            )

        elif custom_llm_provider == "petals" or model in litellm.petals_models:
            api_base = api_base or litellm.api_base

            custom_llm_provider = "petals"
            stream = optional_params.pop("stream", False)
            model_response = petals_handler.completion(
                model=model,
                messages=messages,
                api_base=api_base,
                model_response=model_response,
                print_verbose=print_verbose,
                optional_params=optional_params,
                litellm_params=litellm_params,
                logger_fn=logger_fn,
                encoding=_get_encoding(),
                logging_obj=logging,
                client=client,
            )
            if stream is True:  ## [BETA]
                # Fake streaming for petals
                resp_string = model_response["choices"][0]["message"]["content"]
                response = CustomStreamWrapper(
                    resp_string,
                    model,
                    custom_llm_provider="petals",
                    logging_obj=logging,
                )
                return response
            response = model_response
        elif custom_llm_provider == "snowflake" or model in litellm.snowflake_models:
            try:
                client = (
                    HTTPHandler(timeout=timeout) if stream is False else None
                )  # Keep this here, otherwise, the httpx.client closes and streaming is impossible
                response = base_llm_http_handler.completion(
                    model=model,
                    messages=messages,
                    headers=headers,
                    model_response=model_response,
                    api_key=api_key,
                    api_base=api_base,
                    acompletion=acompletion,
                    logging_obj=logging,
                    optional_params=optional_params,
                    litellm_params=litellm_params,
                    shared_session=shared_session,
                    timeout=timeout,  # type: ignore
                    client=client,
                    custom_llm_provider=custom_llm_provider,
                    encoding=_get_encoding(),
                    stream=stream,
                )

            except Exception as e:
                ## LOGGING - log the original exception returned
                logging.post_call(
                    input=messages,
                    api_key=api_key,
                    original_response=str(e),
                    additional_args={"headers": headers},
                )
                raise e
        elif custom_llm_provider == "gradient_ai":
            api_base = litellm.api_base or api_base
            response = base_llm_http_handler.completion(
                model=model,
                stream=stream,
                messages=messages,
                acompletion=acompletion,
                api_base=api_base,
                model_response=model_response,
                optional_params=optional_params,
                litellm_params=litellm_params,
                shared_session=shared_session,
                custom_llm_provider="gradient_ai",
                timeout=timeout,
                headers=headers,
                encoding=_get_encoding(),
                api_key=api_key,
                logging_obj=logging,
            )

        elif custom_llm_provider == "bytez":
            api_key = (
                api_key
                or litellm.bytez_key
                or get_secret_str("BYTEZ_API_KEY")
                or litellm.api_key
            )

            response = base_llm_http_handler.completion(
                model=model,
                messages=messages,
                headers=headers,
                model_response=model_response,
                api_key=api_key,
                api_base=api_base,
                acompletion=acompletion,
                logging_obj=logging,
                optional_params=optional_params,
                litellm_params=litellm_params,
                timeout=timeout,  # type: ignore
                client=client,
                custom_llm_provider=custom_llm_provider,
                encoding=_get_encoding(),
                stream=stream,
                provider_config=bytez_transformation,
            )

            pass
        elif custom_llm_provider == "lemonade":
            api_key = (
                api_key
                or litellm.lemonade_key
                or get_secret_str("LEMONADE_API_KEY")
                or litellm.api_key
            )

            response = base_llm_http_handler.completion(
                model=model,
                messages=messages,
                headers=headers,
                model_response=model_response,
                api_key=api_key,
                api_base=api_base,
                acompletion=acompletion,
                logging_obj=logging,
                optional_params=optional_params,
                litellm_params=litellm_params,
                timeout=timeout,  # type: ignore
                client=client,
                custom_llm_provider=custom_llm_provider,
                encoding=_get_encoding(),
                stream=stream,
                provider_config=lemonade_transformation,
            )

            pass

        elif custom_llm_provider == "ovhcloud" or model in litellm.ovhcloud_models:
            api_key = (
                api_key
                or litellm.ovhcloud_key
                or get_secret_str("OVHCLOUD_API_KEY")
                or litellm.api_key
            )

            api_base = (
                api_base
                or litellm.api_base
                or get_secret_str("OVHCLOUD_API_BASE")
                or "https://oai.endpoints.kepler.ai.cloud.ovh.net/v1"
            )

            response = base_llm_http_handler.completion(
                model=model,
                messages=messages,
                headers=headers,
                model_response=model_response,
                api_key=api_key,
                api_base=api_base,
                acompletion=acompletion,
                logging_obj=logging,
                optional_params=optional_params,
                litellm_params=litellm_params,
                timeout=timeout,  # type: ignore
                client=client,
                custom_llm_provider=custom_llm_provider,
                encoding=_get_encoding(),
                stream=stream,
                provider_config=ovhcloud_transformation,
            )

            pass

        elif custom_llm_provider == "custom":
            url = litellm.api_base or api_base or ""
            if url is None or url == "":
                raise ValueError(
                    "api_base not set. Set api_base or litellm.api_base for custom endpoints"
                )

            """
            assume input to custom LLM api bases follow this format:
            resp = litellm.module_level_client.post(
                api_base,
                json={
                    'model': 'meta-llama/Llama-2-13b-hf', # model name
                    'params': {
                        'prompt': ["The capital of France is P"],
                        'max_tokens': 32,
                        'temperature': 0.7,
                        'top_p': 1.0,
                        'top_k': 40,
                    }
                }
            )

            """
            prompt = " ".join([message["content"] for message in messages])  # type: ignore
            resp = litellm.module_level_client.post(
                url,
                headers=headers,
                json={
                    "model": model,
                    "params": {
                        "prompt": [prompt],
                        "max_tokens": max_tokens,
                        "temperature": temperature,
                        "top_p": top_p,
                        "top_k": kwargs.get("top_k"),
                    },
                    **kwargs.get("extra_body", {}),
                },
            )
            response_json = resp.json()
            """
            assume all responses from custom api_bases of this format:
            {
                'data': [
                    {
                        'prompt': 'The capital of France is P',
                        'output': ['The capital of France is PARIS.\nThe capital of France is PARIS.\nThe capital of France is PARIS.\nThe capital of France is PARIS.\nThe capital of France is PARIS.\nThe capital of France is PARIS.\nThe capital of France is PARIS.\nThe capital of France is PARIS.\nThe capital of France is PARIS.\nThe capital of France is PARIS.\nThe capital of France is PARIS.\nThe capital of France is PARIS.\nThe capital of France is PARIS.\nThe capital of France'],
                        'params': {'temperature': 0.7, 'top_k': 40, 'top_p': 1}}],
                        'message': 'ok'
                    }
                ]
            }
            """
            string_response = response_json["data"][0]["output"][0]
            ## RESPONSE OBJECT
            model_response.choices[0].message.content = string_response  # type: ignore
            model_response.created = int(time.time())
            model_response.model = model
            response = model_response

        elif (
            custom_llm_provider in litellm._custom_providers
        ):  # Assume custom LLM provider
            # Get the Custom Handler
            custom_handler: Optional[CustomLLM] = None
            for item in litellm.custom_provider_map:
                if item["provider"] == custom_llm_provider:
                    custom_handler = item["custom_handler"]

            if custom_handler is None:
                raise LiteLLMUnknownProvider(
                    model=model, custom_llm_provider=custom_llm_provider
                )

            ## ROUTE LLM CALL ##
            handler_fn = custom_chat_llm_router(
                async_fn=acompletion, stream=stream, custom_llm=custom_handler
            )

            headers = headers or litellm.headers or {}

            ## CALL FUNCTION
            response = handler_fn(
                model=model,
                messages=messages,
                headers=headers,
                model_response=model_response,
                print_verbose=print_verbose,
                api_key=api_key,
                api_base=api_base,
                acompletion=acompletion,
                logging_obj=logging,
                optional_params=optional_params,
                litellm_params=litellm_params,
                logger_fn=logger_fn,
                timeout=timeout,  # type: ignore
                custom_prompt_dict=custom_prompt_dict,
                client=client,  # pass AsyncOpenAI, OpenAI client
                encoding=_get_encoding(),
            )
            if stream is True:
                return CustomStreamWrapper(
                    completion_stream=response,
                    model=model,
                    custom_llm_provider=custom_llm_provider,
                    logging_obj=logging,
                )

        elif custom_llm_provider == "langgraph":
            # LangGraph - Agent Runtime Provider
            from litellm.llms.langgraph.chat.transformation import LangGraphConfig

            (
                api_base,
                api_key,
            ) = LangGraphConfig()._get_openai_compatible_provider_info(
                api_base=api_base or litellm.api_base,
                api_key=api_key or litellm.api_key,
            )

            headers = headers or litellm.headers

            response = base_llm_http_handler.completion(
                model=model,
                stream=stream,
                messages=messages,
                acompletion=acompletion,
                api_base=api_base,
                model_response=model_response,
                optional_params=optional_params,
                litellm_params=litellm_params,
                shared_session=shared_session,
                custom_llm_provider=custom_llm_provider,
                timeout=timeout,
                headers=headers,
                encoding=_get_encoding(),
                api_key=api_key,
                logging_obj=logging,
                client=client,
            )

        elif custom_llm_provider == "langflow":
            # LangFlow - Visual AI Agent Platform
            from litellm.llms.langflow.chat.transformation import LangFlowConfig

            (
                api_base,
                api_key,
            ) = LangFlowConfig()._get_openai_compatible_provider_info(
                api_base=api_base or litellm.api_base,
                api_key=api_key or litellm.api_key,
            )

            headers = headers or litellm.headers

            response = base_llm_http_handler.completion(
                model=model,
                stream=stream,
                messages=messages,
                acompletion=acompletion,
                api_base=api_base,
                model_response=model_response,
                optional_params=optional_params,
                litellm_params=litellm_params,
                shared_session=shared_session,
                custom_llm_provider=custom_llm_provider,
                timeout=timeout,
                headers=headers,
                encoding=_get_encoding(),
                api_key=api_key,
                logging_obj=logging,
                client=client,
            )

        else:
            raise LiteLLMUnknownProvider(
                model=model, custom_llm_provider=custom_llm_provider
            )
        return response
    except Exception as e:
        ## Map to OpenAI Exception
        raise exception_type(
            model=model,
            custom_llm_provider=custom_llm_provider,
            original_exception=e,
            completion_kwargs=args,
            extra_kwargs=kwargs,
        )


def completion(
    model: str,
    messages: list,
    api_base: str,
    model_response: ModelResponse,
    print_verbose: Callable,
    encoding,
    api_key,
    logging_obj,
    optional_params: dict,
    litellm_params=None,
    logger_fn=None,
    default_max_tokens_to_sample=None,
):
    headers = validate_environment(api_key)

    ## Load Config
    config = litellm.AlephAlphaConfig.get_config()
    for k, v in config.items():
        if (
            k not in optional_params
        ):  # completion(top_k=3) > aleph_alpha_config(top_k=3) <- allows for dynamic variables to be passed in
            optional_params[k] = v

    completion_url = api_base
    model = model
    prompt = ""
    if "control" in model:  # follow the ###Instruction / ###Response format
        for idx, message in enumerate(messages):
            if "role" in message:
                if (
                    idx == 0
                ):  # set first message as instruction (required), let later user messages be input
                    prompt += f"###Instruction: {message['content']}"
                else:
                    if message["role"] == "system":
                        prompt += f"###Instruction: {message['content']}"
                    elif message["role"] == "user":
                        prompt += f"###Input: {message['content']}"
                    else:
                        prompt += f"###Response: {message['content']}"
            else:
                prompt += f"{message['content']}"
    else:
        prompt = " ".join(message["content"] for message in messages)
    data = {
        "model": model,
        "prompt": prompt,
        **optional_params,
    }

    ## LOGGING
    logging_obj.pre_call(
        input=prompt,
        api_key=api_key,
        additional_args={"complete_input_dict": data},
    )
    ## COMPLETION CALL
    response = litellm.module_level_client.post(
        completion_url,
        headers=headers,
        data=json.dumps(data),
        stream=optional_params["stream"] if "stream" in optional_params else False,
    )
    if "stream" in optional_params and optional_params["stream"] is True:
        return response.iter_lines()
    else:
        ## LOGGING
        logging_obj.post_call(
            input=prompt,
            api_key=api_key,
            original_response=response.text,
            additional_args={"complete_input_dict": data},
        )
        print_verbose(f"raw model_response: {response.text}")
        ## RESPONSE OBJECT
        completion_response = response.json()
        if "error" in completion_response:
            raise AlephAlphaError(
                message=completion_response["error"],
                status_code=response.status_code,
            )
        else:
            try:
                choices_list = []
                for idx, item in enumerate(completion_response["completions"]):
                    if len(item["completion"]) > 0:
                        message_obj = Message(content=item["completion"])
                    else:
                        message_obj = Message(content=None)
                    choice_obj = Choices(
                        finish_reason=item["finish_reason"],
                        index=idx + 1,
                        message=message_obj,
                    )
                    choices_list.append(choice_obj)
                model_response.choices = choices_list  # type: ignore
            except Exception:
                raise AlephAlphaError(
                    message=json.dumps(completion_response),
                    status_code=response.status_code,
                )

        ## CALCULATING USAGE - baseten charges on time, not tokens - have some mapping of cost here.
        prompt_tokens = len(encoding.encode(prompt))
        completion_tokens = len(
            encoding.encode(
                model_response["choices"][0]["message"]["content"],
                disallowed_special=(),
            )
        )

        model_response.created = int(time.time())
        model_response.model = model
        usage = Usage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
        )
        setattr(model_response, "usage", usage)
        return model_response


def completion(
    model: str,
    messages: list,
    model_response: ModelResponse,
    print_verbose: Callable,
    api_key,
    encoding,
    logging_obj,
    optional_params: dict,
    litellm_params=None,
    logger_fn=None,
):
    try:
        import google.generativeai as palm  # type: ignore
    except Exception:
        raise Exception(
            "Importing google.generativeai failed, please run 'pip install -q google-generativeai"
        )
    palm.configure(api_key=api_key)

    model = model

    ## Load Config
    inference_params = copy.deepcopy(optional_params)
    inference_params.pop(
        "stream", None
    )  # palm does not support streaming, so we handle this by fake streaming in main.py
    config = litellm.PalmConfig.get_config()
    for k, v in config.items():
        if (
            k not in inference_params
        ):  # completion(top_k=3) > palm_config(top_k=3) <- allows for dynamic variables to be passed in
            inference_params[k] = v

    prompt = ""
    for message in messages:
        if "role" in message:
            if message["role"] == "user":
                prompt += f"{message['content']}"
            else:
                prompt += f"{message['content']}"
        else:
            prompt += f"{message['content']}"

    ## LOGGING
    logging_obj.pre_call(
        input=prompt,
        api_key="",
        additional_args={"complete_input_dict": {"inference_params": inference_params}},
    )
    ## COMPLETION CALL
    try:
        response = palm.generate_text(prompt=prompt, **inference_params)  # type: ignore[attr-defined]
    except Exception as e:
        raise PalmError(
            message=str(e),
            status_code=500,
        )

    ## LOGGING
    logging_obj.post_call(
        input=prompt,
        api_key="",
        original_response=response,
        additional_args={"complete_input_dict": {}},
    )
    print_verbose(f"raw model_response: {response}")
    ## RESPONSE OBJECT
    completion_response = response
    try:
        choices_list = []
        for idx, item in enumerate(completion_response.candidates):
            if len(item["output"]) > 0:
                message_obj = Message(content=item["output"])
            else:
                message_obj = Message(content=None)
            choice_obj = Choices(index=idx + 1, message=message_obj)
            choices_list.append(choice_obj)
        model_response.choices = choices_list  # type: ignore
    except Exception:
        raise PalmError(
            message=traceback.format_exc(), status_code=response.status_code
        )

    try:
        completion_response = model_response["choices"][0]["message"].get("content")
    except Exception:
        raise PalmError(
            status_code=400,
            message=f"No response received. Original response - {response}",
        )

    ## CALCULATING USAGE - baseten charges on time, not tokens - have some mapping of cost here.
    prompt_tokens = len(encoding.encode(prompt))
    completion_tokens = len(
        encoding.encode(model_response["choices"][0]["message"].get("content", ""))
    )

    model_response.created = int(time.time())
    model_response.model = "palm/" + model
    usage = Usage(
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=prompt_tokens + completion_tokens,
    )
    setattr(model_response, "usage", usage)
    return model_response


def completion(
    model: str,
    messages: list,
    model_response: ModelResponse,
    print_verbose: Callable,
    encoding,
    logging_obj,
    optional_params: dict,
    vertex_project=None,
    vertex_location=None,
    vertex_credentials=None,
    litellm_params=None,
    logger_fn=None,
    acompletion: bool = False,
):
    """
    NON-GEMINI/ANTHROPIC CALLS.

    This is the handler for OLDER PALM MODELS and VERTEX AI MODEL GARDEN

    For Vertex AI Anthropic: `vertex_anthropic.py`
    For Gemini: `vertex_httpx.py`
    """
    try:
        import vertexai
    except Exception:
        raise VertexAIError(
            status_code=400,
            message="vertexai import failed please run `pip install google-cloud-aiplatform`. This is required for the 'vertex_ai/' route on LiteLLM",
        )

    if not (
        hasattr(vertexai, "preview") or hasattr(vertexai.preview, "language_models")
    ):
        raise VertexAIError(
            status_code=400,
            message="""Upgrade vertex ai. Run `pip install "google-cloud-aiplatform>=1.38"`""",
        )
    try:
        import google.auth  # type: ignore
        from google.cloud import aiplatform  # type: ignore
        from google.cloud.aiplatform_v1beta1.types import (
            content as gapic_content_types,  # type: ignore
        )
        from google.protobuf import json_format  # type: ignore
        from google.protobuf.struct_pb2 import Value  # type: ignore
        from vertexai.language_models import CodeGenerationModel, TextGenerationModel
        from vertexai.preview.generative_models import GenerativeModel
        from vertexai.preview.language_models import ChatModel, CodeChatModel

        ## Load credentials with the correct quota project ref: https://github.com/googleapis/python-aiplatform/issues/2557#issuecomment-1709284744
        print_verbose(
            f"VERTEX AI: vertex_project={vertex_project}; vertex_location={vertex_location}"
        )

        _cache_key = _get_client_cache_key(
            model=model, vertex_project=vertex_project, vertex_location=vertex_location
        )
        _vertex_llm_model_object = _get_client_from_cache(client_cache_key=_cache_key)

        # Load credentials - needed for both vertexai.init() and PredictionServiceClient
        from google.auth.credentials import Credentials

        if vertex_credentials is not None and isinstance(vertex_credentials, str):
            import google.oauth2.service_account

            json_obj = json.loads(vertex_credentials)

            creds = google.oauth2.service_account.Credentials.from_service_account_info(
                json_obj,
                scopes=["https://www.googleapis.com/auth/cloud-platform"],
            )
        else:
            creds, _ = google.auth.default(quota_project_id=vertex_project)

        if _vertex_llm_model_object is None:
            print_verbose(
                f"VERTEX AI: creds={creds}; google application credentials: {os.getenv('GOOGLE_APPLICATION_CREDENTIALS')}"
            )
            vertexai.init(
                project=vertex_project,
                location=vertex_location,
                credentials=cast(Credentials, creds),
            )

        ## Load Config
        config = litellm.VertexAIConfig.get_config()
        for k, v in config.items():
            if k not in optional_params:
                optional_params[k] = v

        ## Process safety settings into format expected by vertex AI
        safety_settings = None
        if "safety_settings" in optional_params:
            safety_settings = optional_params.pop("safety_settings")
            if not isinstance(safety_settings, list):
                raise ValueError("safety_settings must be a list")
            if len(safety_settings) > 0 and not isinstance(safety_settings[0], dict):
                raise ValueError("safety_settings must be a list of dicts")
            safety_settings = [
                gapic_content_types.SafetySetting(x) for x in safety_settings
            ]

        # vertexai does not use an API key, it looks for credentials.json in the environment

        prompt = " ".join(
            [
                message.get("content")
                for message in messages
                if isinstance(message.get("content", None), str)
            ]
        )

        mode = ""

        request_str = ""
        response_obj = None
        instances = None
        client_options = {
            "api_endpoint": f"{vertex_location}-aiplatform.googleapis.com"
        }
        fake_stream = False
        if (
            model in litellm.vertex_language_models
            or model in litellm.vertex_vision_models
        ):
            llm_model: Any = _vertex_llm_model_object or GenerativeModel(model)
            mode = "vision"
            request_str += f"llm_model = GenerativeModel({model})\n"
        elif model in litellm.vertex_chat_models:
            llm_model = _vertex_llm_model_object or ChatModel.from_pretrained(model)
            mode = "chat"
            request_str += f"llm_model = ChatModel.from_pretrained({model})\n"
        elif model in litellm.vertex_text_models:
            llm_model = _vertex_llm_model_object or TextGenerationModel.from_pretrained(
                model
            )
            mode = "text"
            request_str += f"llm_model = TextGenerationModel.from_pretrained({model})\n"
        elif model in litellm.vertex_code_text_models:
            llm_model = _vertex_llm_model_object or CodeGenerationModel.from_pretrained(
                model
            )
            mode = "text"
            request_str += f"llm_model = CodeGenerationModel.from_pretrained({model})\n"
            fake_stream = True
        elif model in litellm.vertex_code_chat_models:  # vertex_code_llm_models
            llm_model = _vertex_llm_model_object or CodeChatModel.from_pretrained(model)
            mode = "chat"
            request_str += f"llm_model = CodeChatModel.from_pretrained({model})\n"
        elif model == "private":
            mode = "private"
            model = optional_params.pop("model_id", None)
            # private endpoint requires a dict instead of JSON
            instances = [optional_params.copy()]
            instances[0]["prompt"] = prompt
            llm_model = aiplatform.PrivateEndpoint(
                endpoint_name=model,
                project=vertex_project,
                location=vertex_location,
            )
            request_str += f"llm_model = aiplatform.PrivateEndpoint(endpoint_name={model}, project={vertex_project}, location={vertex_location})\n"
        else:  # assume vertex model garden on public endpoint
            mode = "custom"

            instances = [optional_params.copy()]
            instances[0]["prompt"] = prompt
            instances = [
                json_format.ParseDict(instance_dict, Value())  # type: ignore[misc]
                for instance_dict in instances
            ]
            # Will determine the API used based on async parameter
            llm_model = None

        # NOTE: async prediction and streaming under "private" mode isn't supported by aiplatform right now
        if acompletion is True:
            data = {
                "llm_model": llm_model,
                "mode": mode,
                "prompt": prompt,
                "logging_obj": logging_obj,
                "request_str": request_str,
                "model": model,
                "model_response": model_response,
                "encoding": encoding,
                "messages": messages,
                "print_verbose": print_verbose,
                "client_options": client_options,
                "instances": instances,
                "vertex_location": vertex_location,
                "vertex_project": vertex_project,
                "vertex_credentials": creds,
                "safety_settings": safety_settings,
                **optional_params,
            }
            if optional_params.get("stream", False) is True:
                # async streaming
                return async_streaming(**data)

            return async_completion(**data)

        completion_response = None

        stream = optional_params.pop(
            "stream", None
        )  # See note above on handling streaming for vertex ai
        if mode == "chat":
            chat = llm_model.start_chat()
            request_str += "chat = llm_model.start_chat()\n"

            if fake_stream is not True and stream is True:
                # NOTE: VertexAI does not accept stream=True as a param and raises an error,
                # we handle this by removing 'stream' from optional params and sending the request
                # after we get the response we add optional_params["stream"] = True, since main.py needs to know it's a streaming response to then transform it for the OpenAI format
                optional_params.pop(
                    "stream", None
                )  # vertex ai raises an error when passing stream in optional params

                request_str += (
                    f"chat.send_message_streaming({prompt}, **{optional_params})\n"
                )
                ## LOGGING
                logging_obj.pre_call(
                    input=prompt,
                    api_key=None,
                    additional_args={
                        "complete_input_dict": optional_params,
                        "request_str": request_str,
                    },
                )

                model_response = chat.send_message_streaming(prompt, **optional_params)

                return model_response

            request_str += f"chat.send_message({prompt}, **{optional_params}).text\n"
            ## LOGGING
            logging_obj.pre_call(
                input=prompt,
                api_key=None,
                additional_args={
                    "complete_input_dict": optional_params,
                    "request_str": request_str,
                },
            )
            completion_response = chat.send_message(prompt, **optional_params).text
        elif mode == "text":
            if fake_stream is not True and stream is True:
                request_str += (
                    f"llm_model.predict_streaming({prompt}, **{optional_params})\n"
                )
                ## LOGGING
                logging_obj.pre_call(
                    input=prompt,
                    api_key=None,
                    additional_args={
                        "complete_input_dict": optional_params,
                        "request_str": request_str,
                    },
                )
                model_response = llm_model.predict_streaming(prompt, **optional_params)

                return model_response

            request_str += f"llm_model.predict({prompt}, **{optional_params}).text\n"
            ## LOGGING
            logging_obj.pre_call(
                input=prompt,
                api_key=None,
                additional_args={
                    "complete_input_dict": optional_params,
                    "request_str": request_str,
                },
            )
            completion_response = llm_model.predict(prompt, **optional_params).text
        elif mode == "custom":
            """
            Vertex AI Model Garden
            """

            if vertex_project is None or vertex_location is None:
                raise ValueError(
                    "Vertex project and location are required for custom endpoint"
                )

            ## LOGGING
            logging_obj.pre_call(
                input=prompt,
                api_key=None,
                additional_args={
                    "complete_input_dict": optional_params,
                    "request_str": request_str,
                },
            )
            llm_model = aiplatform.gapic.PredictionServiceClient(
                client_options=client_options,
                credentials=creds,  # type: ignore[arg-type]
            )
            request_str += f"llm_model = aiplatform.gapic.PredictionServiceClient(client_options={client_options}, credentials=...)\n"
            endpoint_path = llm_model.endpoint_path(
                project=vertex_project, location=vertex_location, endpoint=model
            )
            request_str += (
                f"llm_model.predict(endpoint={endpoint_path}, instances={instances})\n"
            )
            response = llm_model.predict(
                endpoint=endpoint_path, instances=instances
            ).predictions

            completion_response = response[0]
            if (
                isinstance(completion_response, str)
                and "\nOutput:\n" in completion_response
            ):
                completion_response = completion_response.split("\nOutput:\n", 1)[1]
            if stream is True:
                response = TextStreamer(completion_response)
                return response
        elif mode == "private":
            """
            Vertex AI Model Garden deployed on private endpoint
            """
            if instances is None:
                raise ValueError("instances are required for private endpoint")
            if llm_model is None:
                raise ValueError("Unable to pick client for private endpoint")
            ## LOGGING
            logging_obj.pre_call(
                input=prompt,
                api_key=None,
                additional_args={
                    "complete_input_dict": optional_params,
                    "request_str": request_str,
                },
            )
            request_str += f"llm_model.predict(instances={instances})\n"
            response = llm_model.predict(instances=instances).predictions

            completion_response = response[0]
            if (
                isinstance(completion_response, str)
                and "\nOutput:\n" in completion_response
            ):
                completion_response = completion_response.split("\nOutput:\n", 1)[1]
            if stream is True:
                response = TextStreamer(completion_response)
                return response

        ## LOGGING
        logging_obj.post_call(
            input=prompt, api_key=None, original_response=completion_response
        )

        ## RESPONSE OBJECT
        if isinstance(completion_response, litellm.Message):
            model_response.choices[0].message = completion_response  # type: ignore
        elif len(str(completion_response)) > 0:
            model_response.choices[0].message.content = str(completion_response)  # type: ignore
        model_response.created = int(time.time())
        model_response.model = model
        ## CALCULATING USAGE
        if model in litellm.vertex_language_models and response_obj is not None:
            model_response.choices[0].finish_reason = map_finish_reason(  # type: ignore[assignment]
                response_obj.candidates[0].finish_reason.name
            )
            usage = Usage(
                prompt_tokens=response_obj.usage_metadata.prompt_token_count,
                completion_tokens=response_obj.usage_metadata.candidates_token_count,
                total_tokens=response_obj.usage_metadata.total_token_count,
            )
        else:
            # init prompt tokens
            # this block attempts to get usage from response_obj if it exists, if not it uses the litellm token counter
            prompt_tokens, completion_tokens, _ = 0, 0, 0
            if response_obj is not None:
                if hasattr(response_obj, "usage_metadata") and hasattr(
                    response_obj.usage_metadata, "prompt_token_count"
                ):
                    prompt_tokens = response_obj.usage_metadata.prompt_token_count
                    completion_tokens = (
                        response_obj.usage_metadata.candidates_token_count
                    )
            else:
                prompt_tokens = len(encoding.encode(prompt))
                completion_tokens = len(
                    encoding.encode(
                        model_response["choices"][0]["message"].get("content", "")
                    )
                )

            usage = Usage(
                prompt_tokens=prompt_tokens,
                completion_tokens=completion_tokens,
                total_tokens=prompt_tokens + completion_tokens,
            )
        setattr(model_response, "usage", usage)

        if fake_stream is True and stream is True:
            return ModelResponseIterator(model_response)
        return model_response
    except Exception as e:
        if isinstance(e, VertexAIError):
            raise e
        raise litellm.APIConnectionError(
            message=str(e), llm_provider="vertex_ai", model=model
        )


def completion(
    model: str,
    messages: list,
    model_response: ModelResponse,
    print_verbose: Callable,
    encoding,
    logging_obj,
    optional_params: dict,
    custom_prompt_dict={},
    litellm_params=None,
    logger_fn=None,
):
    global llm
    try:
        llm, SamplingParams = validate_environment(model=model)
    except Exception as e:
        raise VLLMError(status_code=0, message=str(e))
    sampling_params = SamplingParams(**optional_params)
    if model in custom_prompt_dict:
        # check if the model has a registered custom prompt
        model_prompt_details = custom_prompt_dict[model]
        prompt = custom_prompt(
            role_dict=model_prompt_details["roles"],
            initial_prompt_value=model_prompt_details["initial_prompt_value"],
            final_prompt_value=model_prompt_details["final_prompt_value"],
            messages=messages,
        )
    else:
        prompt = prompt_factory(model=model, messages=messages)

    ## LOGGING
    logging_obj.pre_call(
        input=prompt,
        api_key="",
        additional_args={"complete_input_dict": sampling_params},
    )

    if llm:
        outputs = llm.generate(prompt, sampling_params)
    else:
        raise VLLMError(
            status_code=0, message="Need to pass in a model name to initialize vllm"
        )

    ## COMPLETION CALL
    if "stream" in optional_params and optional_params["stream"] is True:
        return iter(outputs)
    else:
        ## LOGGING
        logging_obj.post_call(
            input=prompt,
            api_key="",
            original_response=outputs,
            additional_args={"complete_input_dict": sampling_params},
        )
        print_verbose(f"raw model_response: {outputs}")
        ## RESPONSE OBJECT
        model_response.choices[0].message.content = outputs[0].outputs[0].text  # type: ignore

        ## CALCULATING USAGE
        prompt_tokens = len(outputs[0].prompt_token_ids)
        completion_tokens = len(outputs[0].outputs[0].token_ids)

        model_response.created = int(time.time())
        model_response.model = model
        usage = Usage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
        )
        setattr(model_response, "usage", usage)
        return model_response


def completion(
    model: str,
    messages: list,
    api_base: str,
    model_response: ModelResponse,
    print_verbose: Callable,
    optional_params: dict,
    litellm_params: dict,
    logging_obj,
    api_key,
    encoding,
    custom_prompt_dict={},
    logger_fn=None,
    acompletion=None,
    headers={},
) -> Union[ModelResponse, CustomStreamWrapper]:
    headers = replicate_config.validate_environment(
        api_key=api_key,
        headers=headers,
        model=model,
        messages=messages,
        optional_params=optional_params,
        litellm_params=litellm_params,
    )
    # Start a prediction and get the prediction URL
    version_id = replicate_config.model_to_version_id(model)
    input_data = replicate_config.transform_request(
        model=model,
        messages=messages,
        optional_params=optional_params,
        litellm_params=litellm_params,
        headers=headers,
    )

    if acompletion is not None and acompletion is True:
        return async_completion(
            model_response=model_response,
            model=model,
            encoding=encoding,
            messages=messages,
            optional_params=optional_params,
            litellm_params=litellm_params,
            version_id=version_id,
            input_data=input_data,
            api_key=api_key,
            api_base=api_base,
            logging_obj=logging_obj,
            print_verbose=print_verbose,
            headers=headers,
        )  # type: ignore
    ## COMPLETION CALL
    model_response.created = int(
        time.time()
    )  # for pricing this must remain right before calling api

    prediction_url = replicate_config.get_complete_url(
        api_base=api_base,
        api_key=api_key,
        model=model,
        optional_params=optional_params,
        litellm_params=litellm_params,
    )

    ## COMPLETION CALL
    httpx_client = _get_httpx_client(
        params={"timeout": 600.0},
    )
    response = httpx_client.post(
        url=prediction_url,
        headers=headers,
        data=json.dumps(input_data),
    )

    prediction_url = replicate_config.get_prediction_url(response)

    # Handle the prediction response (streaming or non-streaming)
    if "stream" in optional_params and optional_params["stream"] is True:
        print_verbose("streaming request")
        _response = handle_prediction_response_streaming(
            prediction_url,
            api_key,
            print_verbose,
            headers=headers,
            http_client=httpx_client,
        )
        return CustomStreamWrapper(_response, model, logging_obj=logging_obj, custom_llm_provider="replicate")  # type: ignore
    else:
        for retry in range(litellm.DEFAULT_REPLICATE_POLLING_RETRIES):
            time.sleep(
                litellm.DEFAULT_REPLICATE_POLLING_DELAY_SECONDS + 2 * retry
            )  # wait to allow response to be generated by replicate - else partial output is generated with status=="processing"
            response = httpx_client.get(url=prediction_url, headers=headers)
            if response.status_code == 200 and response.json().get("status") in [
                "processing",
                "starting",
            ]:
                continue
            return litellm.ReplicateConfig().transform_response(
                model=model,
                raw_response=response,
                model_response=model_response,
                logging_obj=logging_obj,
                api_key=api_key,
                request_data=input_data,
                messages=messages,
                optional_params=optional_params,
                litellm_params=litellm_params,
                encoding=encoding,
            )

    raise ReplicateError(
        status_code=500,
        message="No response received from Replicate API after max retries",
        headers=None,
    )


def completion(
    model: str,
    messages: list,
    api_base: Optional[str],
    model_response: ModelResponse,
    print_verbose: Callable,
    encoding,
    logging_obj,
    optional_params: dict,
    stream=False,
    litellm_params=None,
    logger_fn=None,
    client: Optional[Union[HTTPHandler, AsyncHTTPHandler]] = None,
):
    ## Load Config
    config = litellm.PetalsConfig.get_config()
    for k, v in config.items():
        if (
            k not in optional_params
        ):  # completion(top_k=3) > petals_config(top_k=3) <- allows for dynamic variables to be passed in
            optional_params[k] = v

    if model in litellm.custom_prompt_dict:
        # check if the model has a registered custom prompt
        model_prompt_details = litellm.custom_prompt_dict[model]
        prompt = custom_prompt(
            role_dict=model_prompt_details["roles"],
            initial_prompt_value=model_prompt_details["initial_prompt_value"],
            final_prompt_value=model_prompt_details["final_prompt_value"],
            messages=messages,
        )
    else:
        prompt = prompt_factory(model=model, messages=messages)

    output_text: Optional[str] = None
    if api_base:
        ## LOGGING
        logging_obj.pre_call(
            input=prompt,
            api_key="",
            additional_args={
                "complete_input_dict": optional_params,
                "api_base": api_base,
            },
        )
        data = {"model": model, "inputs": prompt, **optional_params}

        ## COMPLETION CALL
        if client is None or not isinstance(client, HTTPHandler):
            client = _get_httpx_client()
        response = client.post(api_base, data=data)

        ## LOGGING
        logging_obj.post_call(
            input=prompt,
            api_key="",
            original_response=response.text,
            additional_args={"complete_input_dict": optional_params},
        )

        ## RESPONSE OBJECT
        try:
            output_text = response.json()["outputs"]
        except Exception as e:
            PetalsError(
                status_code=response.status_code,
                message=str(e),
                headers=response.headers,
            )

    else:
        try:
            from petals import AutoDistributedModelForCausalLM  # type: ignore
            from transformers import AutoTokenizer
        except Exception:
            raise Exception(
                "Importing torch, transformers, petals failed\nTry pip installing petals \npip install git+https://github.com/bigscience-workshop/petals"
            )

        model = model

        tokenizer = AutoTokenizer.from_pretrained(
            model, use_fast=False, add_bos_token=False
        )
        model_obj = AutoDistributedModelForCausalLM.from_pretrained(model)

        ## LOGGING
        logging_obj.pre_call(
            input=prompt,
            api_key="",
            additional_args={"complete_input_dict": optional_params},
        )

        ## COMPLETION CALL
        inputs = tokenizer(prompt, return_tensors="pt")["input_ids"]

        # optional params: max_new_tokens=1,temperature=0.9, top_p=0.6
        outputs = model_obj.generate(inputs, **optional_params)

        ## LOGGING
        logging_obj.post_call(
            input=prompt,
            api_key="",
            original_response=outputs,
            additional_args={"complete_input_dict": optional_params},
        )
        ## RESPONSE OBJECT
        output_text = tokenizer.decode(outputs[0])

    if output_text is not None and len(output_text) > 0:
        model_response.choices[0].message.content = output_text  # type: ignore

    prompt_tokens = len(encoding.encode(prompt))
    completion_tokens = len(
        encoding.encode(model_response["choices"][0]["message"].get("content"))
    )

    model_response.created = int(time.time())
    model_response.model = model
    usage = Usage(
        prompt_tokens=prompt_tokens,
        completion_tokens=completion_tokens,
        total_tokens=prompt_tokens + completion_tokens,
    )
    setattr(model_response, "usage", usage)
    return model_response


def completion(
    model: str,
    messages: list,
    api_base: Optional[str],
    model_response: ModelResponse,
    print_verbose: Callable,
    encoding,
    api_key,
    logging_obj,
    optional_params: dict,
    litellm_params: dict,
    custom_prompt_dict={},
    logger_fn=None,
    default_max_tokens_to_sample=None,
):
    headers = oobabooga_config.validate_environment(
        api_key=api_key,
        headers={},
        model=model,
        messages=messages,
        optional_params=optional_params,
        litellm_params=litellm_params,
    )
    if "https" in model:
        completion_url = model
    elif api_base:
        completion_url = api_base
    else:
        raise OobaboogaError(
            status_code=404,
            message="API Base not set. Set one via completion(..,api_base='your-api-url')",
        )
    model = model

    completion_url = completion_url + "/v1/chat/completions"
    data = oobabooga_config.transform_request(
        model=model,
        messages=messages,
        optional_params=optional_params,
        litellm_params=litellm_params,
        headers=headers,
    )
    ## LOGGING

    logging_obj.pre_call(
        input=messages,
        api_key=api_key,
        additional_args={"complete_input_dict": data},
    )
    ## COMPLETION CALL
    client = _get_httpx_client()
    response = client.post(
        completion_url,
        headers=headers,
        data=json.dumps(data),
        stream=optional_params["stream"] if "stream" in optional_params else False,
    )
    if "stream" in optional_params and optional_params["stream"] is True:
        return response.iter_lines()
    else:
        return oobabooga_config.transform_response(
            model=model,
            raw_response=response,
            model_response=model_response,
            logging_obj=logging_obj,
            api_key=api_key,
            request_data=data,
            messages=messages,
            optional_params=optional_params,
            litellm_params=litellm_params,
            encoding=encoding,
        )


def completion(
    model: str,
    messages: list,
    api_base: str,
    model_response: ModelResponse,
    print_verbose: Callable,
    encoding,
    api_key,
    logging_obj,
    optional_params: dict,
    litellm_params: dict,
    logger_fn=None,
    default_max_tokens_to_sample=None,
    client: Optional[Union[HTTPHandler, AsyncHTTPHandler]] = None,
    headers={},
):
    headers = nlp_config.validate_environment(
        api_key=api_key,
        headers=headers,
        model=model,
        messages=messages,
        optional_params=optional_params,
        litellm_params=litellm_params,
    )

    ## Load Config
    config = litellm.NLPCloudConfig.get_config()
    for k, v in config.items():
        if (
            k not in optional_params
        ):  # completion(top_k=3) > togetherai_config(top_k=3) <- allows for dynamic variables to be passed in
            optional_params[k] = v

    completion_url_fragment_1 = api_base
    completion_url_fragment_2 = "/generation"
    model = model

    completion_url = completion_url_fragment_1 + model + completion_url_fragment_2
    data = nlp_config.transform_request(
        model=model,
        messages=messages,
        optional_params=optional_params,
        litellm_params=litellm_params,
        headers=headers,
    )

    ## LOGGING
    logging_obj.pre_call(
        input=None,
        api_key=api_key,
        additional_args={
            "complete_input_dict": data,
            "headers": headers,
            "api_base": completion_url,
        },
    )
    ## COMPLETION CALL
    if client is None or not isinstance(client, HTTPHandler):
        client = _get_httpx_client()

    response = client.post(
        completion_url,
        headers=headers,
        data=json.dumps(data),
        stream=optional_params["stream"] if "stream" in optional_params else False,
    )
    if "stream" in optional_params and optional_params["stream"] is True:
        return clean_and_iterate_chunks(response)
    else:
        return nlp_config.transform_response(
            model=model,
            raw_response=response,
            model_response=model_response,
            logging_obj=logging_obj,
            api_key=api_key,
            request_data=data,
            messages=messages,
            optional_params=optional_params,
            litellm_params=litellm_params,
            encoding=encoding,
        )

