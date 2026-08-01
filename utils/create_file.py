
def create_file(
    file: FileTypes,
    purpose: Literal["assistants", "batch", "fine-tune", "messages"],
    expires_after: Optional[FileExpiresAfter] = None,
    custom_llm_provider: Optional[FileCreateProvider] = None,
    extra_headers: Optional[Dict[str, str]] = None,
    extra_body: Optional[Dict[str, str]] = None,
    **kwargs,
) -> Union[OpenAIFileObject, Coroutine[Any, Any, OpenAIFileObject]]:
    """
    Files are used to upload documents that can be used with features like Assistants, Fine-tuning, and Batch API.

    LiteLLM Equivalent of POST: POST https://api.openai.com/v1/files

    Specify either provider_list or custom_llm_provider.
    """
    try:
        _is_async = kwargs.pop("acreate_file", False) is True
        optional_params = GenericLiteLLMParams(**kwargs)
        litellm_params_dict = dict(**kwargs)
        logging_obj = cast(
            Optional[LiteLLMLoggingObj], kwargs.get("litellm_logging_obj")
        )
        if logging_obj is None:
            raise ValueError("logging_obj is required")
        client = kwargs.get("client")

        ### TIMEOUT LOGIC ###
        timeout = optional_params.timeout or kwargs.get("request_timeout", 600) or 600
        # set timeout for 10 minutes by default

        if (
            timeout is not None
            and isinstance(timeout, httpx.Timeout)
            and supports_httpx_timeout(cast(str, custom_llm_provider)) is False
        ):
            read_timeout = timeout.read or 600
            timeout = read_timeout  # default 10 min timeout
        elif timeout is not None and not isinstance(timeout, httpx.Timeout):
            timeout = float(timeout)  # type: ignore
        elif timeout is None:
            timeout = 600.0

        if expires_after is not None:
            _create_file_request = CreateFileRequest(
                file=file,
                purpose=purpose,
                expires_after=expires_after,
                extra_headers=extra_headers,
                extra_body=extra_body,
            )
        else:
            _create_file_request = CreateFileRequest(
                file=file,
                purpose=purpose,
                extra_headers=extra_headers,
                extra_body=extra_body,
            )

        provider_config = ProviderConfigManager.get_provider_files_config(
            model="",
            provider=LlmProviders(custom_llm_provider),
        )
        if provider_config is not None:
            response = base_llm_http_handler.create_file(
                provider_config=provider_config,
                litellm_params=litellm_params_dict,
                create_file_data=_create_file_request,
                headers=extra_headers or {},
                api_base=optional_params.api_base,
                api_key=optional_params.api_key,
                logging_obj=logging_obj,
                _is_async=_is_async,
                client=(
                    client
                    if client is not None
                    and isinstance(client, (HTTPHandler, AsyncHTTPHandler))
                    else None
                ),
                timeout=timeout,
            )
        elif custom_llm_provider in OPENAI_COMPATIBLE_BATCH_AND_FILES_PROVIDERS:
            openai_creds = get_openai_credentials(
                api_base=optional_params.api_base,
                api_key=optional_params.api_key,
                organization=optional_params.organization,
            )
            response = openai_files_instance.create_file(
                _is_async=_is_async,
                api_base=openai_creds.api_base,
                api_key=openai_creds.api_key,
                timeout=timeout,
                max_retries=optional_params.max_retries,
                organization=openai_creds.organization,
                create_file_data=_create_file_request,
            )
        elif custom_llm_provider == "azure":
            azure_creds = get_azure_credentials(
                api_base=optional_params.api_base,
                api_key=optional_params.api_key,
                api_version=optional_params.api_version,
            )
            response = azure_files_instance.create_file(
                _is_async=_is_async,
                api_base=azure_creds.api_base,
                api_key=azure_creds.api_key,
                api_version=azure_creds.api_version,
                timeout=timeout,
                max_retries=optional_params.max_retries,
                create_file_data=_create_file_request,
                litellm_params=litellm_params_dict,
            )
        else:
            raise litellm.exceptions.BadRequestError(
                message="LiteLLM doesn't support {} for 'create_file'. Only ['openai', 'azure', 'vertex_ai', 'manus', 'anthropic'] are supported.".format(
                    custom_llm_provider
                ),
                model="n/a",
                llm_provider=custom_llm_provider,
                response=httpx.Response(
                    status_code=400,
                    content="Unsupported provider",
                    request=httpx.Request(method="create_file", url="https://github.com/BerriAI/litellm"),  # type: ignore
                ),
            )
        return response
    except Exception as e:
        raise e

