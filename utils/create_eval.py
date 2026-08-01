
def create_eval(
    data_source_config: Dict[str, Any],
    testing_criteria: List[Dict[str, Any]],
    name: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    custom_llm_provider: Optional[str] = None,
    **kwargs,
) -> Union[Eval, Coroutine[Any, Any, Eval]]:
    """
    Create a new evaluation

    Args:
        data_source_config: Configuration for the data source
        testing_criteria: List of graders for all eval runs
        name: Optional name for the evaluation
        metadata: Optional additional metadata (max 16 key-value pairs)
        extra_headers: Additional headers for the request
        extra_query: Additional query parameters
        extra_body: Additional body parameters
        timeout: Request timeout
        custom_llm_provider: Provider name (e.g., 'openai')
        **kwargs: Additional parameters

    Returns:
        Eval object
    """
    local_vars = locals()
    try:
        litellm_logging_obj: LiteLLMLoggingObj = kwargs.get("litellm_logging_obj")  # type: ignore
        litellm_call_id: Optional[str] = kwargs.get("litellm_call_id", None)
        _is_async = kwargs.pop("acreate_eval", False) is True

        # Get LiteLLM parameters
        litellm_params = GenericLiteLLMParams(**kwargs)

        # Determine provider
        if custom_llm_provider is None:
            custom_llm_provider = "openai"

        # Get provider config
        evals_api_provider_config: Optional[BaseEvalsAPIConfig] = (
            ProviderConfigManager.get_provider_evals_api_config(  # type: ignore
                provider=litellm.LlmProviders(custom_llm_provider),
            )
        )

        if evals_api_provider_config is None:
            raise ValueError(f"CREATE eval is not supported for {custom_llm_provider}")

        # Build create request
        create_request: CreateEvalRequest = {
            "data_source_config": data_source_config,  # type: ignore
            "testing_criteria": testing_criteria,  # type: ignore
        }
        if name is not None:
            create_request["name"] = name

        # Merge extra_body if provided
        if extra_body:
            create_request.update(extra_body)  # type: ignore

        # Validate environment and get headers
        headers = extra_headers or {}
        headers = evals_api_provider_config.validate_environment(
            headers=headers, litellm_params=litellm_params
        )

        # Transform request
        request_body = evals_api_provider_config.transform_create_eval_request(
            create_request=create_request,
            litellm_params=litellm_params,
            headers=headers,
        )

        # Get API base and URL
        api_base = litellm_params.api_base or DEFAULT_OPENAI_API_BASE
        url = evals_api_provider_config.get_complete_url(
            api_base=api_base, endpoint="evals"
        )

        # Pre-call logging
        litellm_logging_obj.update_from_kwargs(
            kwargs=kwargs,
            model=None,
            optional_params=request_body,
            litellm_params={
                "litellm_call_id": litellm_call_id,
            },
            custom_llm_provider=custom_llm_provider,
        )

        # Make HTTP request
        response = base_llm_http_handler.create_eval_handler(  # type: ignore
            url=url,
            request_body=request_body,
            evals_api_provider_config=evals_api_provider_config,
            custom_llm_provider=custom_llm_provider,
            litellm_params=litellm_params,
            logging_obj=litellm_logging_obj,
            extra_headers=headers,
            timeout=timeout or request_timeout,
            _is_async=_is_async,
            client=kwargs.get("client"),
            shared_session=kwargs.get("shared_session"),
        )

        return response
    except Exception as e:
        raise litellm.exception_type(
            model=None,
            custom_llm_provider=custom_llm_provider,
            original_exception=e,
            completion_kwargs=local_vars,
            extra_kwargs=kwargs,
        )

