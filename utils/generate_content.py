
def generate_content(
    model: str,
    contents: GenerateContentContentListUnionDict,
    config: Optional[GenerateContentConfigDict] = None,
    tools: Optional[ToolConfigDict] = None,
    # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
    # The extra values given here take precedence over values defined on the client or passed to this method.
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    # LiteLLM specific params,
    custom_llm_provider: Optional[str] = None,
    **kwargs,
) -> Any:
    """
    Generate content using Google GenAI
    """
    local_vars = locals()
    try:
        _is_async = kwargs.pop("agenerate_content", False)

        # Handle generationConfig parameter from kwargs for backward compatibility
        if "generationConfig" in kwargs and config is None:
            config = kwargs.pop("generationConfig")
        # Check for mock response first
        litellm_params = GenericLiteLLMParams(**kwargs)
        if litellm_params.mock_response and isinstance(
            litellm_params.mock_response, str
        ):
            return GenerateContentHelper.mock_generate_content_response(
                mock_response=litellm_params.mock_response
            )

        # Setup the call
        setup_result = GenerateContentHelper.setup_generate_content_call(
            model=model,
            contents=contents,
            config=config,
            custom_llm_provider=custom_llm_provider,
            tools=tools,
            **kwargs,
        )

        # Extract systemInstruction from kwargs to pass to handler
        system_instruction = kwargs.get("systemInstruction") or kwargs.get(
            "system_instruction"
        )

        # Check if we should use the adapter (when provider config is None)
        if setup_result.generate_content_provider_config is None:
            # Use the adapter to convert to completion format
            return GenerateContentToCompletionHandler.generate_content_handler(
                model=model,
                contents=contents,  # type: ignore
                config=setup_result.generate_content_config_dict,
                tools=tools,
                _is_async=_is_async,
                litellm_params=setup_result.litellm_params,
                extra_headers=extra_headers,
                **kwargs,
            )

        # Call the standard handler
        response = base_llm_http_handler.generate_content_handler(
            model=setup_result.model,
            contents=contents,
            tools=tools,
            generate_content_provider_config=setup_result.generate_content_provider_config,
            generate_content_config_dict=setup_result.generate_content_config_dict,
            custom_llm_provider=setup_result.custom_llm_provider,
            litellm_params=setup_result.litellm_params,
            logging_obj=setup_result.litellm_logging_obj,
            extra_headers=extra_headers,
            extra_body=extra_body,
            timeout=timeout or request_timeout,
            _is_async=_is_async,
            client=kwargs.get("client"),
            litellm_metadata=kwargs.get("litellm_metadata", {}),
            system_instruction=system_instruction,
        )

        return response
    except Exception as e:
        raise litellm.exception_type(
            model=model,
            custom_llm_provider=custom_llm_provider,
            original_exception=e,
            completion_kwargs=local_vars,
            extra_kwargs=kwargs,
        )

