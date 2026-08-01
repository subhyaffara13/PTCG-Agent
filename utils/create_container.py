
def create_container(
    name: str,
    expires_after: Optional[Dict[str, Any]] = None,
    file_ids: Optional[List[str]] = None,
    timeout=600,  # default to 10 minutes
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    api_version: Optional[str] = None,
    custom_llm_provider: Literal["openai", "azure", "azure_text"] = "openai",
    *,
    acreate_container: Literal[True],
    **kwargs,
) -> Coroutine[Any, Any, ContainerObject]:
    ...


def create_container(
    name: str,
    expires_after: Optional[Dict[str, Any]] = None,
    file_ids: Optional[List[str]] = None,
    timeout=600,  # default to 10 minutes
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    api_version: Optional[str] = None,
    custom_llm_provider: Literal["openai", "azure", "azure_text"] = "openai",
    *,
    acreate_container: Literal[False] = False,
    **kwargs,
) -> ContainerObject:
    ...


def create_container(
    name: str,
    expires_after: Optional[Dict[str, Any]] = None,
    file_ids: Optional[List[str]] = None,
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
    ContainerObject,
    Coroutine[Any, Any, ContainerObject],
]:
    """Create a container using the OpenAI Container API.

    Currently supports OpenAI

    Example:
    ```python
    import litellm

    response = litellm.create_container(
        name="My Container",
        custom_llm_provider="openai",
    )
    print(response)
    ```
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

            response = ContainerObject(**mock_response)
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
                f"container operations are not supported for {custom_llm_provider}"
            )

        local_vars.update(kwargs)
        # Get ContainerCreateOptionalRequestParams with only valid parameters
        container_create_optional_params: ContainerCreateOptionalRequestParams = (
            ContainerRequestUtils.get_requested_container_create_optional_param(
                local_vars
            )
        )

        # Get optional parameters for the container API
        container_create_request_params: Dict = (
            ContainerRequestUtils.get_optional_params_container_create(
                container_provider_config=container_provider_config,
                container_create_optional_params=container_create_optional_params,
            )
        )

        # Pre Call logging
        litellm_logging_obj.update_from_kwargs(
            kwargs=kwargs,
            model="",
            optional_params=dict(container_create_request_params),
            litellm_params={
                "litellm_call_id": litellm_call_id,
                **container_create_request_params,
            },
            custom_llm_provider=custom_llm_provider,
        )

        # Set the correct call type for container creation
        litellm_logging_obj.call_type = CallTypes.create_container.value

        container_obj = base_llm_http_handler.container_create_handler(
            name=name,
            container_create_request_params=container_create_request_params,
            container_provider_config=container_provider_config,
            litellm_params=litellm_params,
            logging_obj=litellm_logging_obj,
            extra_headers=extra_headers,
            timeout=timeout or DEFAULT_REQUEST_TIMEOUT,
            _is_async=_is_async,
        )

        # Encode container_id with provider/model metadata for routing
        if isinstance(container_obj, ContainerObject):
            container_obj = ContainerRequestUtils.encode_container_id_in_response(
                response_obj=container_obj,
                custom_llm_provider=custom_llm_provider,
                litellm_metadata=kwargs.get("litellm_metadata"),
                extra_body=extra_body,
            )

        return container_obj

    except Exception as e:
        raise litellm.exception_type(
            model="",
            custom_llm_provider=custom_llm_provider,
            original_exception=e,
            completion_kwargs=local_vars,
            extra_kwargs=kwargs,
        )

