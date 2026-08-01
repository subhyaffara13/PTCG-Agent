
def file_content(
    file_id: str,
    model: Optional[str] = None,
    custom_llm_provider: Optional[Union[FileContentProvider, str]] = None,
    extra_headers: Optional[Dict[str, str]] = None,
    extra_body: Optional[Dict[str, str]] = None,
    chunk_size: int = 1024 * 1024,
    stream: bool = False,
    **kwargs,
) -> Union[
    HttpxBinaryResponseContent,
    FileContentStreamingResult,
    Coroutine[Any, Any, HttpxBinaryResponseContent],
    Coroutine[Any, Any, FileContentStreamingResult],
]:
    """
    Returns the contents of the specified file.

    LiteLLM Equivalent of POST: POST https://api.openai.com/v1/files
    """
    try:
        optional_params = GenericLiteLLMParams(**kwargs)
        litellm_params_dict = get_litellm_params(**kwargs)
        _add_trusted_model_credentials_to_litellm_params(
            litellm_params_dict=litellm_params_dict,
            kwargs=kwargs,
        )
        ### TIMEOUT LOGIC ###
        timeout = optional_params.timeout or kwargs.get("request_timeout", 600) or 600
        client = kwargs.get("client")
        # set timeout for 10 minutes by default

        try:
            if model is not None:
                _, custom_llm_provider, _, _ = get_llm_provider(
                    model, custom_llm_provider
                )
        except Exception:
            pass

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

        _file_content_request = FileContentRequest(
            file_id=file_id,
            extra_headers=extra_headers,
            extra_body=extra_body,
        )

        _is_async = kwargs.pop("afile_content", False) is True

        if stream and _should_sdk_support_streaming(custom_llm_provider):
            return file_content_streaming(
                file_id=file_id,
                model=model,
                custom_llm_provider=custom_llm_provider,
                extra_headers=extra_headers,
                extra_body=extra_body,
                chunk_size=chunk_size,
                optional_params=optional_params,
                timeout=timeout,
                logging_obj=cast(
                    Optional[LiteLLMLoggingObj], kwargs.get("litellm_logging_obj")
                ),
                _is_async=_is_async,
                client=client,
            )

        # Check if provider has a custom files config (e.g., Anthropic, Manus)
        provider_config = ProviderConfigManager.get_provider_files_config(
            model="",
            provider=LlmProviders(custom_llm_provider),
        )
        if provider_config is not None:
            litellm_params_dict["api_key"] = optional_params.api_key
            litellm_params_dict["api_base"] = optional_params.api_base

            logging_obj = kwargs.get("litellm_logging_obj")
            if logging_obj is None:
                logging_obj = LiteLLMLoggingObj(
                    model="",
                    messages=[],
                    stream=False,
                    call_type="afile_content" if _is_async else "file_content",
                    start_time=time.time(),
                    litellm_call_id=kwargs.get(
                        "litellm_call_id", str(uuid_module.uuid4())
                    ),
                    function_id=str(kwargs.get("id") or ""),
                )

            response = base_llm_http_handler.retrieve_file_content(
                file_content_request=_file_content_request,
                provider_config=provider_config,
                litellm_params=litellm_params_dict,
                headers=extra_headers or {},
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
            return response

        if custom_llm_provider in OPENAI_COMPATIBLE_BATCH_AND_FILES_PROVIDERS:
            openai_creds = get_openai_credentials(
                api_base=optional_params.api_base,
                api_key=optional_params.api_key,
                organization=optional_params.organization,
            )
            response = openai_files_instance.file_content(
                _is_async=_is_async,
                file_content_request=_file_content_request,
                api_base=openai_creds.api_base,
                api_key=openai_creds.api_key,
                timeout=timeout,
                max_retries=optional_params.max_retries,
                organization=openai_creds.organization,
            )
        elif custom_llm_provider == "azure":
            azure_creds = get_azure_credentials(
                api_base=optional_params.api_base,
                api_key=optional_params.api_key,
                api_version=optional_params.api_version,
            )
            response = azure_files_instance.file_content(
                _is_async=_is_async,
                api_base=azure_creds.api_base,
                api_key=azure_creds.api_key,
                api_version=azure_creds.api_version,
                timeout=timeout,
                max_retries=optional_params.max_retries,
                file_content_request=_file_content_request,
                client=client,
                litellm_params=litellm_params_dict,
            )
        elif custom_llm_provider == "vertex_ai":
            api_base = optional_params.api_base or ""
            vertex_ai_project = (
                optional_params.vertex_project
                or litellm.vertex_project
                or get_secret_str("VERTEXAI_PROJECT")
            )
            vertex_ai_location = (
                optional_params.vertex_location
                or litellm.vertex_location
                or get_secret_str("VERTEXAI_LOCATION")
            )
            vertex_credentials = optional_params.vertex_credentials or get_secret_str(
                "VERTEXAI_CREDENTIALS"
            )

            response = vertex_ai_files_instance.file_content(
                _is_async=_is_async,
                file_content_request=_file_content_request,
                api_base=api_base,
                vertex_credentials=vertex_credentials,
                vertex_project=vertex_ai_project,
                vertex_location=vertex_ai_location,
                timeout=timeout,
                max_retries=optional_params.max_retries,
                litellm_params=litellm_params_dict,
            )
        elif custom_llm_provider == "bedrock":
            response = bedrock_files_instance.file_content(
                _is_async=_is_async,
                file_content_request=_file_content_request,
                api_base=optional_params.api_base,
                optional_params=litellm_params_dict,
                timeout=timeout,
                max_retries=optional_params.max_retries,
            )
        else:
            raise litellm.exceptions.BadRequestError(
                message="LiteLLM doesn't support {} for 'file_content'. Supported providers are 'openai', 'azure', 'vertex_ai', 'bedrock', 'manus', 'anthropic'.".format(
                    custom_llm_provider
                ),
                model="n/a",
                llm_provider=custom_llm_provider,
                response=httpx.Response(
                    status_code=400,
                    content="Unsupported provider",
                    request=httpx.Request(method="create_thread", url="https://github.com/BerriAI/litellm"),  # type: ignore
                ),
            )
        return response
    except Exception as e:
        raise e

