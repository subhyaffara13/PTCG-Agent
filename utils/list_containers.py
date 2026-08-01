
def list_containers(
    after: Optional[str] = None,
    limit: Optional[int] = None,
    order: Optional[str] = None,
    timeout=600,  # default to 10 minutes
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    api_version: Optional[str] = None,
    custom_llm_provider: Literal["openai", "azure", "azure_text"] = "openai",
    *,
    alist_containers: Literal[True],
    **kwargs,
) -> Coroutine[Any, Any, ContainerListResponse]:
    ...


def list_containers(
    after: Optional[str] = None,
    limit: Optional[int] = None,
    order: Optional[str] = None,
    timeout=600,  # default to 10 minutes
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    api_version: Optional[str] = None,
    custom_llm_provider: Literal["openai", "azure", "azure_text"] = "openai",
    *,
    alist_containers: Literal[False] = False,
    **kwargs,
) -> ContainerListResponse:
    ...


def list_containers(
    after: Optional[str] = None,
    limit: Optional[int] = None,
    order: Optional[str] = None,
    timeout=600,  # default to 10 minutes
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    api_version: Optional[str] = None,
    custom_llm_provider: Literal["openai", "azure", "azure_text"] = "openai",
    # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
    # The extra values given here take precedence over values defined on the client or passed to this method.
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    **kwargs,
) -> Union[
    ContainerListResponse,
    Coroutine[Any, Any, ContainerListResponse],
]:
    """List containers using the OpenAI Container API.

    Currently supports OpenAI
    """
    local_vars = locals()
    try:
        litellm_logging_obj: LiteLLMLoggingObj = kwargs.pop("litellm_logging_obj")  # type: ignore
        litellm_call_id: Optional[str] = kwargs.get("litellm_call_id")
        _is_async = kwargs.pop("async_call", False) is True

        # Check for mock response first
        mock_response = kwargs.get("mock_response")
        if mock_response is not None:
            if isinstance(mock_response, str):
                mock_response = json.loads(mock_response)

            response = ContainerListResponse(**mock_response)
            return response

        # get llm provider logic
        # Pass credential params explicitly since they're named args, not in kwargs
        litellm_params = GenericLiteLLMParams(
            api_key=api_key,
            api_base=api_base,
            api_version=api_version,
            **kwargs,
        )
        # get provider config
        container_provider_config: Optional[BaseContainerConfig] = (
            ProviderConfigManager.get_provider_container_config(
                provider=litellm.LlmProviders(custom_llm_provider),
            )
        )

        if container_provider_config is None:
            raise ValueError(
                f"Container provider config not found for provider: {custom_llm_provider}"
            )

        # Get container list request parameters
        container_list_optional_params: ContainerListOptionalRequestParams = (
            ContainerRequestUtils.get_requested_container_list_optional_param(
                local_vars
            )
        )

        # Pre Call logging
        litellm_logging_obj.update_from_kwargs(
            kwargs=kwargs,
            model="",
            optional_params=dict(container_list_optional_params),
            litellm_params={
                "litellm_call_id": litellm_call_id,
                **container_list_optional_params,
            },
            custom_llm_provider=custom_llm_provider,
        )

        # Set the correct call type
        litellm_logging_obj.call_type = CallTypes.list_containers.value

        return base_llm_http_handler.container_list_handler(
            container_provider_config=container_provider_config,
            litellm_params=litellm_params,
            logging_obj=litellm_logging_obj,
            after=after,
            limit=limit,
            order=order,
            extra_headers=extra_headers,
            extra_query=extra_query,
            timeout=timeout or DEFAULT_REQUEST_TIMEOUT,
            _is_async=_is_async,
        )

    except Exception as e:
        raise litellm.exception_type(
            model="",
            custom_llm_provider=custom_llm_provider,
            original_exception=e,
            completion_kwargs=local_vars,
            extra_kwargs=kwargs,
        )

