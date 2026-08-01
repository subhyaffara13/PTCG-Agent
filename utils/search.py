
def search(pattern, string, flags=0, pos=None, endpos=None, partial=False,
  concurrent=None, timeout=None, ignore_unused=False, **kwargs):
    """Search through string looking for a match to the pattern, returning a
    match object, or None if no match was found."""
    pat = _compile(pattern, flags, ignore_unused, kwargs, True)
    return pat.search(string, pos, endpos, concurrent, partial, timeout)


def search(
    query: Union[str, List[str]],
    search_provider: str,
    max_results: Optional[int] = None,
    search_domain_filter: Optional[List[str]] = None,
    max_tokens_per_page: Optional[int] = None,
    country: Optional[str] = None,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    extra_headers: Optional[Dict[str, Any]] = None,
    **kwargs,
) -> Union[SearchResponse, Coroutine[Any, Any, SearchResponse]]:
    """
    Synchronous Search function.

    Args:
        query: Search query (string or list of strings)
        search_provider: Provider name (e.g., "perplexity")
        max_results: Optional maximum number of results (1-20), default 10
        search_domain_filter: Optional list of domains to filter (max 20)
        max_tokens_per_page: Optional max tokens per page, default 1024
        country: Optional country code filter (e.g., 'US', 'GB', 'DE')
        api_key: Optional API key
        api_base: Optional API base URL
        timeout: Optional timeout
        extra_headers: Optional extra headers
        **kwargs: Additional parameters

    Returns:
        SearchResponse with results list following Perplexity format

    Example:
        ```python
        import litellm

        # Basic search
        response = litellm.search(
            query="latest AI developments 2024",
            search_provider="perplexity"
        )

        # Search with options
        response = litellm.search(
            query="AI developments",
            search_provider="perplexity",
            max_results=10,
            search_domain_filter=["arxiv.org", "nature.com"],
            max_tokens_per_page=1024,
            country="US"
        )

        # Multi-query search
        response = litellm.search(
            query=["AI developments", "machine learning trends"],
            search_provider="perplexity"
        )

        # Access results
        for result in response.results:
            print(f"{result.title}: {result.url}")
            print(f"Snippet: {result.snippet}")
            if result.date:
                print(f"Date: {result.date}")
        ```
    """
    local_vars = locals()
    try:
        litellm_logging_obj: LiteLLMLoggingObj = kwargs.pop("litellm_logging_obj")  # type: ignore
        litellm_call_id: Optional[str] = kwargs.get("litellm_call_id", None)
        _is_async = kwargs.pop("asearch", False) is True

        # Validate query parameter
        if not isinstance(query, (str, list)):
            raise ValueError(
                f"query must be a string or list of strings, got {type(query)}"
            )

        if isinstance(query, list) and not all(isinstance(q, str) for q in query):
            raise ValueError("All items in query list must be strings")

        # Get provider config
        search_provider_config: Optional[BaseSearchConfig] = (
            ProviderConfigManager.get_provider_search_config(
                provider=SearchProviders(search_provider),
            )
        )

        if search_provider_config is None:
            raise ValueError(f"Search is not supported for provider: {search_provider}")

        verbose_logger.debug(f"Search call - provider: {search_provider}")

        # Build optional_params from explicit parameters
        optional_params = _build_search_optional_params(
            max_results=max_results,
            search_domain_filter=search_domain_filter,
            max_tokens_per_page=max_tokens_per_page,
            country=country,
        )

        # Filter out internal LiteLLM parameters from kwargs
        filtered_kwargs = filter_out_litellm_params(kwargs=kwargs)

        # Add remaining kwargs to optional_params (for provider-specific params)
        for key, value in filtered_kwargs.items():
            if key not in optional_params:
                optional_params[key] = value

        verbose_logger.debug(f"Search optional_params: {optional_params}")

        # Validate environment and get headers
        headers = search_provider_config.validate_environment(
            api_key=api_key,
            api_base=api_base,
            headers=extra_headers or {},
        )

        # Get complete URL
        complete_url = search_provider_config.get_complete_url(
            api_base=api_base,
            optional_params=optional_params,
            api_key=api_key,
        )

        # Pre Call logging
        model_name = f"{search_provider}/search"
        litellm_logging_obj.update_from_kwargs(
            kwargs=kwargs,
            model=model_name,
            optional_params=optional_params,
            litellm_params={
                "litellm_call_id": litellm_call_id,
                "api_base": complete_url,
            },
            custom_llm_provider=search_provider,
        )

        # Call the handler
        response = base_llm_http_handler.search(
            query=query,
            optional_params=optional_params,
            timeout=timeout or request_timeout,
            logging_obj=litellm_logging_obj,
            api_key=api_key,
            api_base=complete_url,
            custom_llm_provider=search_provider,
            asearch=_is_async,
            headers=headers,
            provider_config=search_provider_config,
        )

        return response
    except Exception as e:
        model_name = f"{search_provider}/search"
        raise litellm.exception_type(
            model=model_name,
            custom_llm_provider=search_provider,
            original_exception=e,
            completion_kwargs=local_vars,
            extra_kwargs=kwargs,
        )


def search(
    vector_store_id: str,
    query: Union[str, List[str]],
    filters: Optional[Dict] = None,
    max_num_results: Optional[int] = None,
    ranking_options: Optional[Dict] = None,
    rewrite_query: Optional[bool] = None,
    # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
    # The extra values given here take precedence over values defined on the client or passed to this method.
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    # LiteLLM specific params,
    custom_llm_provider: Optional[str] = None,
    **kwargs,
) -> Union[VectorStoreSearchResponse, Coroutine[Any, Any, VectorStoreSearchResponse]]:
    """
    Search a vector store for relevant chunks based on a query and file attributes filter.

    Args:
        vector_store_id: The ID of the vector store to search.
        query: A query string or array for the search.
        filters: Optional filter to apply based on file attributes.
        max_num_results: Maximum number of results to return (1-50, default 10).
        ranking_options: Optional ranking options for search.
        rewrite_query: Whether to rewrite the natural language query for vector search.

    Returns:
        VectorStoreSearchResponse containing the search results.
    """
    local_vars = locals()
    try:
        litellm_logging_obj: LiteLLMLoggingObj = kwargs.get("litellm_logging_obj")  # type: ignore
        litellm_call_id: Optional[str] = kwargs.get("litellm_call_id", None)
        _is_async = kwargs.pop("asearch", False) is True

        # pull credentials from registry if available
        if litellm.vector_store_registry is not None and vector_store_id is not None:
            try:
                registry_credentials = (
                    litellm.vector_store_registry.get_credentials_for_vector_store(
                        vector_store_id
                    )
                )
                kwargs.update(registry_credentials)
            except Exception:
                pass

        # get llm provider logic
        litellm_params = GenericLiteLLMParams(vector_store_id=vector_store_id, **kwargs)

        ## MOCK RESPONSE LOGIC
        if litellm_params.mock_response and isinstance(
            litellm_params.mock_response, (str, builtins.list)
        ):
            mock_results = None
            if isinstance(litellm_params.mock_response, builtins.list):
                mock_results = litellm_params.mock_response  # type: ignore[assignment]
            return mock_vector_store_search_response(mock_results=mock_results)

        # Default to OpenAI for vector stores
        if custom_llm_provider is None:
            custom_llm_provider = "openai"

        if "/" in custom_llm_provider:
            api_type, custom_llm_provider, _, _ = get_llm_provider(
                model=custom_llm_provider,
                custom_llm_provider=None,
                litellm_params=None,
            )
        else:
            api_type = None
            custom_llm_provider = custom_llm_provider

        # get provider config - using vector store custom logger for now
        vector_store_provider_config = (
            ProviderConfigManager.get_provider_vector_stores_config(
                provider=litellm.LlmProviders(custom_llm_provider),
                api_type=api_type,
            )
        )

        if vector_store_provider_config is None:
            raise ValueError(
                f"Vector store search is not supported for {custom_llm_provider}"
            )

        local_vars.update(kwargs)

        # Get VectorStoreSearchOptionalRequestParams with only valid parameters
        vector_store_search_optional_params: VectorStoreSearchOptionalRequestParams = (
            VectorStoreRequestUtils.get_requested_vector_store_search_optional_param(
                local_vars,
                vector_store_provider_config=vector_store_provider_config,
            )
        )

        # Pre Call logging
        litellm_logging_obj.update_from_kwargs(
            kwargs=kwargs,
            model=api_type,
            optional_params={
                "vector_store_id": vector_store_id,
                "query": query,
                **vector_store_search_optional_params,
            },
            litellm_params={
                "litellm_call_id": litellm_call_id,
                "vector_store_id": vector_store_id,
                **litellm_params.model_dump(exclude_none=True),
            },
            custom_llm_provider=custom_llm_provider,
        )

        response = base_llm_http_handler.vector_store_search_handler(
            vector_store_id=vector_store_id,
            query=query,
            vector_store_search_optional_params=vector_store_search_optional_params,
            vector_store_provider_config=vector_store_provider_config,
            custom_llm_provider=custom_llm_provider,
            litellm_params=litellm_params,
            logging_obj=litellm_logging_obj,
            extra_headers=extra_headers,
            extra_body=extra_body,
            timeout=timeout or request_timeout,
            _is_async=_is_async,
            client=kwargs.get("client"),
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

