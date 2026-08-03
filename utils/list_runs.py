from typing import Any, Dict, Optional, Union

def list_runs(
    eval_id: str,
    limit: Optional[int] = None,
    after: Optional[str] = None,
    before: Optional[str] = None,
    order: Optional[str] = None,
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    custom_llm_provider: Optional[str] = None,
    **kwargs,
) -> Union[ListRunsResponse, Coroutine[Any, Any, ListRunsResponse]]:
    """
    List all runs for an evaluation

    Args:
        eval_id: The ID of the evaluation
        limit: Number of results to return per page (max 100, default 20)
        after: Cursor for pagination - returns runs after this ID
        before: Cursor for pagination - returns runs before this ID
        order: Sort order ('asc' or 'desc', default 'desc')
        extra_headers: Additional headers for the request
        extra_query: Additional query parameters
        timeout: Request timeout
        custom_llm_provider: Provider name (e.g., 'openai')
        **kwargs: Additional parameters

    Returns:
        ListRunsResponse object
    """
    local_vars = locals()
    try:
        litellm_logging_obj: LiteLLMLoggingObj = kwargs.get("litellm_logging_obj")  # type: ignore
        litellm_call_id: Optional[str] = kwargs.get("litellm_call_id", None)
        _is_async = kwargs.pop("alist_runs", False) is True

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
            raise ValueError(f"LIST runs is not supported for {custom_llm_provider}")

        # Build list parameters
        list_params: ListRunsParams = {}
        if limit is not None:
            list_params["limit"] = limit
        if after is not None:
            list_params["after"] = after
        if before is not None:
            list_params["before"] = before
        if order is not None:
            list_params["order"] = order  # type: ignore

        # Merge extra_query if provided
        if extra_query:
            list_params.update(extra_query)  # type: ignore

        # Validate environment and get headers
        headers = extra_headers or {}
        headers = evals_api_provider_config.validate_environment(
            headers=headers, litellm_params=litellm_params
        )

        # Transform request
        url, query_params = evals_api_provider_config.transform_list_runs_request(
            eval_id=eval_id,
            list_params=list_params,
            litellm_params=litellm_params,
            headers=headers,
        )

        # Pre-call logging
        litellm_logging_obj.update_from_kwargs(
            kwargs=kwargs,
            model=None,
            optional_params={"eval_id": eval_id, **query_params},
            litellm_params={
                "litellm_call_id": litellm_call_id,
            },
            custom_llm_provider=custom_llm_provider,
        )

        # Make HTTP request
        response = base_llm_http_handler.list_runs_handler(  # type: ignore
            url=url,
            query_params=query_params,
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

