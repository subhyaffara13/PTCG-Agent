
def responses(
    input: Union[str, ResponseInputParam],
    model: str,
    include: Optional[List[ResponseIncludable]] = None,
    instructions: Optional[str] = None,
    max_output_tokens: Optional[int] = None,
    prompt: Optional[PromptObject] = None,
    metadata: Optional[Dict[str, Any]] = None,
    parallel_tool_calls: Optional[bool] = None,
    previous_response_id: Optional[str] = None,
    reasoning: Optional[Reasoning] = None,
    store: Optional[bool] = None,
    background: Optional[bool] = None,
    stream: Optional[bool] = None,
    temperature: Optional[float] = None,
    text: Optional["ResponseText"] = None,
    text_format: Optional[Union[Type["BaseModel"], dict]] = None,
    tool_choice: Optional[ToolChoice] = None,
    tools: Optional[Iterable[ToolParam]] = None,
    top_p: Optional[float] = None,
    truncation: Optional[Literal["auto", "disabled"]] = None,
    user: Optional[str] = None,
    service_tier: Optional[str] = None,
    safety_identifier: Optional[str] = None,
    # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
    # The extra values given here take precedence over values defined on the client or passed to this method.
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    # LiteLLM specific params,
    allowed_openai_params: Optional[List[str]] = None,
    custom_llm_provider: Optional[str] = None,
    **kwargs,
):
    """
    Synchronous version of the Responses API.
    Uses the synchronous HTTP handler to make requests.
    """
    local_vars = locals()

    try:
        litellm_logging_obj: LiteLLMLoggingObj = kwargs.get("litellm_logging_obj")  # type: ignore
        litellm_call_id: Optional[str] = kwargs.get("litellm_call_id", None)
        _is_async = kwargs.pop("aresponses", False) is True
        use_chat_completions_api = _pop_use_chat_completions_api_kw(kwargs)

        # Convert text_format to text parameter if provided
        text = ResponsesAPIRequestUtils.convert_text_format_to_text_param(
            text_format=text_format, text=text
        )
        if text is not None:
            # Update local_vars to include the converted text parameter
            local_vars["text"] = text

        # get llm provider logic
        litellm_params = GenericLiteLLMParams(**kwargs)

        #########################################################
        # MOCK RESPONSE LOGIC
        #########################################################
        if litellm_params.mock_response and isinstance(
            litellm_params.mock_response, str
        ):
            return mock_responses_api_response(
                mock_response=litellm_params.mock_response
            )

        _stripped_model, _from_chat_completions_prefix = (
            _normalize_openai_chat_completions_responses_model(model)
        )
        model = _stripped_model
        local_vars["model"] = model
        use_chat_completions_api = (
            use_chat_completions_api or _from_chat_completions_prefix
        )

        model, custom_llm_provider = _resolve_model_provider_for_responses(
            model=model,
            custom_llm_provider=custom_llm_provider,
            litellm_params=litellm_params,
            local_vars=local_vars,
        )

        #########################################################
        # PROMPT MANAGEMENT
        # If aresponses() already ran the async hook, it pops prompt_id and
        # passes the result via _async_prompt_merged_params — apply those
        # directly and skip the sync hook to avoid double-merging.
        #########################################################
        input, model, custom_llm_provider = _apply_prompt_management_to_responses_call(
            input=input,
            model=model,
            custom_llm_provider=custom_llm_provider,
            litellm_logging_obj=litellm_logging_obj,
            kwargs=kwargs,
            local_vars=local_vars,
        )

        #########################################################
        # Update input and tools with provider-specific file IDs if managed files are used
        #########################################################
        input, tools = _apply_managed_file_id_mapping(
            input=input, tools=tools, kwargs=kwargs, local_vars=local_vars
        )

        #########################################################
        # Native MCP Responses API
        #########################################################
        _mcp_dispatch = _responses_try_dispatch_mcp_gateway(
            tools=tools,
            input=input,
            model=model,
            include=include,
            instructions=instructions,
            max_output_tokens=max_output_tokens,
            prompt=prompt,
            metadata=metadata,
            parallel_tool_calls=parallel_tool_calls,
            previous_response_id=previous_response_id,
            reasoning=reasoning,
            store=store,
            background=background,
            stream=stream,
            temperature=temperature,
            text=text,
            tool_choice=tool_choice,
            top_p=top_p,
            truncation=truncation,
            user=user,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            custom_llm_provider=custom_llm_provider,
            kwargs=kwargs,
            _is_async=_is_async,
        )
        if _mcp_dispatch is not None:
            return _mcp_dispatch

        # get provider config
        responses_api_provider_config: Optional[BaseResponsesAPIConfig]
        if custom_llm_provider is None:
            responses_api_provider_config = None
        else:
            responses_api_provider_config = (
                ProviderConfigManager.get_provider_responses_api_config(
                    model=model,
                    provider=custom_llm_provider,
                )
            )

        local_vars.update(kwargs)
        # Map reasoning_effort (from litellm_params/proxy config) to reasoning when not set
        if reasoning is None and "reasoning_effort" in local_vars:
            _mapped = LiteLLMResponsesTransformationHandler()._map_reasoning_effort(
                local_vars.pop("reasoning_effort")
            )
            if _mapped is not None:
                reasoning = _mapped
                local_vars["reasoning"] = _mapped
        # Get ResponsesAPIOptionalRequestParams with only valid parameters
        response_api_optional_params: ResponsesAPIOptionalRequestParams = (
            ResponsesAPIRequestUtils.get_requested_response_api_optional_param(
                local_vars
            )
        )

        _file_search_dispatch = _responses_try_dispatch_emulated_file_search(
            tools=tools,
            input=input,
            model=model,
            responses_api_provider_config=responses_api_provider_config,
            use_chat_completions_api=use_chat_completions_api,
            include=include,
            instructions=instructions,
            max_output_tokens=max_output_tokens,
            prompt=prompt,
            metadata=metadata,
            parallel_tool_calls=parallel_tool_calls,
            previous_response_id=previous_response_id,
            reasoning=reasoning,
            store=store,
            background=background,
            stream=stream,
            temperature=temperature,
            text=text,
            tool_choice=tool_choice,
            top_p=top_p,
            truncation=truncation,
            user=user,
            service_tier=service_tier,
            safety_identifier=safety_identifier,
            text_format=text_format,
            allowed_openai_params=allowed_openai_params,
            extra_headers=extra_headers,
            extra_query=extra_query,
            extra_body=extra_body,
            timeout=timeout,
            custom_llm_provider=custom_llm_provider,
            kwargs=kwargs,
            _is_async=_is_async,
        )
        if _file_search_dispatch is not None:
            return _file_search_dispatch

        if responses_api_provider_config is None or use_chat_completions_api is True:
            return litellm_completion_transformation_handler.response_api_handler(
                model=model,
                input=input,
                responses_api_request=response_api_optional_params,
                custom_llm_provider=custom_llm_provider,
                _is_async=_is_async,
                stream=stream,
                extra_headers=extra_headers,
                extra_body=extra_body,
                timeout=timeout if timeout is not None else request_timeout,
                **kwargs,
            )

        # Get optional parameters for the responses API
        responses_api_request_params: Dict = (
            ResponsesAPIRequestUtils.get_optional_params_responses_api(
                model=model,
                responses_api_provider_config=responses_api_provider_config,
                response_api_optional_params=response_api_optional_params,
                allowed_openai_params=allowed_openai_params,
            )
        )

        litellm_logging_obj.update_from_kwargs(
            kwargs=kwargs,
            model=model,
            user=user,
            optional_params=dict(responses_api_request_params),
            litellm_params={
                **responses_api_request_params,
                "aresponses": _is_async,
                "litellm_call_id": litellm_call_id,
                "model_info": kwargs.get("model_info"),
                "data_residency": infer_openai_data_residency(
                    custom_llm_provider, litellm_params.api_base
                ),
                "metadata": (
                    kwargs["litellm_metadata"]
                    if "litellm_metadata" in kwargs
                    else kwargs.get("metadata")
                ),
            },
            custom_llm_provider=custom_llm_provider,
        )

        # Decode any litellm-encoded encrypted-content item IDs back to their original IDs
        input = ResponsesAPIRequestUtils._restore_encrypted_content_item_ids_in_input(
            input
        )

        # Call the handler with _is_async flag instead of directly calling the async handler
        if custom_llm_provider is None:
            raise ValueError("custom_llm_provider is required but passed as None")

        response = base_llm_http_handler.response_api_handler(
            model=model,
            input=input,
            responses_api_provider_config=responses_api_provider_config,
            response_api_optional_request_params=responses_api_request_params,
            custom_llm_provider=custom_llm_provider,
            litellm_params=litellm_params,
            logging_obj=litellm_logging_obj,
            extra_headers=extra_headers,
            extra_body=extra_body,
            timeout=timeout or request_timeout,
            _is_async=_is_async,
            client=kwargs.get("client"),
            fake_stream=responses_api_provider_config.should_fake_stream(
                model=model, stream=stream, custom_llm_provider=custom_llm_provider
            ),
            litellm_metadata=kwargs.get("litellm_metadata", {}),
            shared_session=kwargs.get("shared_session"),
        )

        # Update the responses_api_response_id with the model_id
        if isinstance(response, ResponsesAPIResponse):
            response = ResponsesAPIRequestUtils._update_responses_api_response_id_with_model_id(
                responses_api_response=response,
                litellm_metadata=kwargs.get("litellm_metadata", {}),
                custom_llm_provider=custom_llm_provider,
            )
            # Stamp custom_llm_provider so callbacks can identify the provider
            # (mirrors litellm/main.py:1371 for chat completions)
            response._hidden_params["custom_llm_provider"] = custom_llm_provider

        return response
    except Exception as e:
        raise litellm.exception_type(
            model=model,
            custom_llm_provider=custom_llm_provider,
            original_exception=e,
            completion_kwargs=local_vars,
            extra_kwargs=kwargs,
        )

