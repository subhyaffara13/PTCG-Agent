
def upload_container_file(
    container_id: str,
    file: FileTypes,
    timeout=600,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    api_version: Optional[str] = None,
    custom_llm_provider: Literal["openai", "azure", "azure_text"] = "openai",
    *,
    aupload_container_file: Literal[True],
    **kwargs,
) -> Coroutine[Any, Any, ContainerFileObject]:
    ...


def upload_container_file(
    container_id: str,
    file: FileTypes,
    timeout=600,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    api_version: Optional[str] = None,
    custom_llm_provider: Literal["openai", "azure", "azure_text"] = "openai",
    *,
    aupload_container_file: Literal[False] = False,
    **kwargs,
) -> ContainerFileObject:
    ...


def upload_container_file(
    container_id: str,
    file: FileTypes,
    timeout=600,  # default to 10 minutes
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    api_version: Optional[str] = None,
    custom_llm_provider: Literal["openai", "azure", "azure_text"] = "openai",
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    **kwargs,
) -> Union[
    ContainerFileObject,
    Coroutine[Any, Any, ContainerFileObject],
]:
    """Upload a file to a container using the OpenAI Container API.

    This endpoint allows uploading files directly to a container session,
    supporting various file types like CSV, Excel, Python scripts, JSON, etc.
    This is useful when /chat/completions or /responses sends files to the
    container but the input file type is limited to PDF. This endpoint lets
    you work with other file types.

    Currently supports OpenAI

    Example:
    ```python
    import litellm

    # Upload a CSV file
    response = litellm.upload_container_file(
        container_id="container_abc123",
        file=("data.csv", open("data.csv", "rb").read(), "text/csv"),
        custom_llm_provider="openai",
    )
    print(response)

    # Upload a Python script
    response = litellm.upload_container_file(
        container_id="container_abc123",
        file=("script.py", b"print('hello world')", "text/x-python"),
        custom_llm_provider="openai",
    )
    print(response)
    ```
    """
    from litellm.llms.custom_httpx.container_handler import generic_container_handler

    local_vars = locals()
    try:
        resolved_custom_llm_provider: str = custom_llm_provider
        litellm_logging_obj: LiteLLMLoggingObj = kwargs.pop("litellm_logging_obj")  # type: ignore
        litellm_call_id: Optional[str] = kwargs.get("litellm_call_id")
        _is_async = kwargs.pop("async_call", False) is True

        # Check for mock response first
        mock_response = kwargs.get("mock_response")
        if mock_response is not None:
            if isinstance(mock_response, str):
                mock_response = json.loads(mock_response)

            response = ContainerFileObject(**mock_response)
            return response

        # get llm provider logic
        # Pass credential params explicitly since they're named args, not in kwargs
        litellm_params = GenericLiteLLMParams(
            api_key=api_key,
            api_base=api_base,
            api_version=api_version,
            **kwargs,
        )

        # Decode container ID and extract provider info
        original_container_id, resolved_custom_llm_provider, litellm_params = (
            decode_managed_container_id_for_request(
                container_id=container_id,
                custom_llm_provider=custom_llm_provider,
                litellm_params=litellm_params,
            )
        )

        # get provider config
        container_provider_config: Optional[BaseContainerConfig] = (
            ProviderConfigManager.get_provider_container_config(
                provider=litellm.LlmProviders(resolved_custom_llm_provider),
            )
        )

        if container_provider_config is None:
            raise ValueError(
                f"Container provider config not found for provider: {resolved_custom_llm_provider}"
            )

        # Pre Call logging
        litellm_logging_obj.update_from_kwargs(
            kwargs=kwargs,
            model="",
            optional_params={"container_id": container_id},
            litellm_params={
                "litellm_call_id": litellm_call_id,
            },
            custom_llm_provider=resolved_custom_llm_provider,
        )

        # Set the correct call type
        litellm_logging_obj.call_type = CallTypes.upload_container_file.value

        return generic_container_handler.handle(
            endpoint_name="upload_container_file",
            container_provider_config=container_provider_config,
            litellm_params=litellm_params,
            logging_obj=litellm_logging_obj,
            extra_headers=extra_headers,
            extra_query=extra_query,
            timeout=timeout or DEFAULT_REQUEST_TIMEOUT,
            _is_async=_is_async,
            container_id=original_container_id,  # Use decoded original ID
            file=file,
        )

    except Exception as e:
        raise litellm.exception_type(
            model="",
            custom_llm_provider=resolved_custom_llm_provider,
            original_exception=e,
            completion_kwargs=local_vars,
            extra_kwargs=kwargs,
        )

