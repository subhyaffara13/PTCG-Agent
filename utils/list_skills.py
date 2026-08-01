
def list_skills(
    limit: Optional[int] = None,
    page: Optional[str] = None,
    source: Optional[str] = None,
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    custom_llm_provider: Optional[str] = None,
    **kwargs,
) -> Union[ListSkillsResponse, Coroutine[Any, Any, ListSkillsResponse]]:
    """
    List all skills

    Args:
        limit: Number of results to return per page (max 100, default 20)
        page: Pagination token for fetching a specific page of results
        source: Filter skills by source ('custom' or 'anthropic')
        extra_headers: Additional headers for the request
        extra_query: Additional query parameters
        timeout: Request timeout
        custom_llm_provider: Provider name (e.g., 'anthropic')
        **kwargs: Additional parameters

    Returns:
        ListSkillsResponse object
    """
    local_vars = locals()
    try:
        litellm_logging_obj: LiteLLMLoggingObj = kwargs.get("litellm_logging_obj")  # type: ignore
        litellm_call_id: Optional[str] = kwargs.get("litellm_call_id", None)
        _is_async = kwargs.pop("alist_skills", False) is True

        # Get LiteLLM parameters
        litellm_params = GenericLiteLLMParams(**kwargs)

        # Determine provider
        if custom_llm_provider is None:
            custom_llm_provider = "anthropic"

        # Route to LiteLLM DB if custom_llm_provider="litellm_proxy"
        if custom_llm_provider == LlmProviders.LITELLM_PROXY.value:
            return _get_litellm_skills_handler().list_skills_handler(
                limit=limit or 20,
                offset=0,
                user_api_key_dict=_get_user_api_key_auth_from_kwargs(kwargs),
                _is_async=_is_async,
                logging_obj=litellm_logging_obj,
                litellm_call_id=litellm_call_id,
            )

        # Get provider config for external providers (Anthropic, etc.)
        skills_api_provider_config: Optional[BaseSkillsAPIConfig] = (
            ProviderConfigManager.get_provider_skills_api_config(
                provider=litellm.LlmProviders(custom_llm_provider),
            )
        )

        if skills_api_provider_config is None:
            raise ValueError(f"LIST skills is not supported for {custom_llm_provider}")

        # Build list parameters
        list_params: ListSkillsParams = {}
        if limit is not None:
            list_params["limit"] = limit
        if page is not None:
            list_params["page"] = page
        if source is not None:
            list_params["source"] = source

        # Merge extra_query if provided
        if extra_query:
            list_params.update(extra_query)  # type: ignore

        # Validate environment and get headers
        headers = extra_headers or {}
        headers = skills_api_provider_config.validate_environment(
            headers=headers, litellm_params=litellm_params
        )

        # Transform request
        url, query_params = skills_api_provider_config.transform_list_skills_request(
            list_params=list_params,
            litellm_params=litellm_params,
            headers=headers,
        )

        # Pre-call logging
        litellm_logging_obj.update_from_kwargs(
            kwargs=kwargs,
            model=None,
            optional_params=query_params,
            litellm_params={
                "litellm_call_id": litellm_call_id,
            },
            custom_llm_provider=custom_llm_provider,
        )

        # Make HTTP request
        response = base_llm_http_handler.list_skills_handler(
            url=url,
            query_params=query_params,
            skills_api_provider_config=skills_api_provider_config,
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

