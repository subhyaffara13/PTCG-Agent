from typing import Any, Dict, Optional, Union

def create_run(
    eval_id: str,
    data_source: Dict[str, Any],
    name: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    custom_llm_provider: Optional[str] = None,
    **kwargs,
) -> Union[Run, Coroutine[Any, Any, Run]]:
    """
    Create a new run for an evaluation

    Args:
        eval_id: The ID of the evaluation to run
        data_source: Data source configuration for the run (can be jsonl, completions, or responses type)
        name: Optional name for the run
        metadata: Optional additional metadata
        extra_headers: Additional headers for the request
        extra_query: Additional query parameters
        extra_body: Additional body parameters
        timeout: Request timeout (default 600s for long-running operations)
        custom_llm_provider: Provider name (e.g., 'openai')
        **kwargs: Additional parameters

    Returns:
        Run object
    """
    local_vars = locals()
    try:
        litellm_logging_obj: LiteLLMLoggingObj = kwargs.get("litellm_logging_obj")  # type: ignore
        litellm_call_id: Optional[str] = kwargs.get("litellm_call_id", None)
        _is_async = kwargs.pop("acreate_run", False) is True

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
            raise ValueError(f"CREATE run is not supported for {custom_llm_provider}")

        # Build create request
        create_request: CreateRunRequest = {
            "data_source": data_source,  # type: ignore
        }
        if name is not None:
            create_request["name"] = name
        # if metadata is not None:
        #     create_request["metadata"] = metadata

        # Merge extra_body if provided
        if extra_body:
            create_request.update(extra_body)  # type: ignore

        # Validate environment and get headers
        headers = extra_headers or {}
        headers = evals_api_provider_config.validate_environment(
            headers=headers, litellm_params=litellm_params
        )

        # Transform request
        api_base = litellm_params.api_base or DEFAULT_OPENAI_API_BASE
        url, request_body = evals_api_provider_config.transform_create_run_request(
            eval_id=eval_id,
            create_request=create_request,
            litellm_params=litellm_params,
            headers=headers,
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

        # Make HTTP request (default 600s timeout for long-running operations)
        response = base_llm_http_handler.create_run_handler(  # type: ignore
            url=url,
            request_body=request_body,
            evals_api_provider_config=evals_api_provider_config,
            custom_llm_provider=custom_llm_provider,
            litellm_params=litellm_params,
            logging_obj=litellm_logging_obj,
            extra_headers=headers,
            timeout=timeout or httpx.Timeout(timeout=600.0, connect=5.0),
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

