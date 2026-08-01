
def create_batch(
    completion_window: Literal["24h"],
    endpoint: Literal["/v1/chat/completions", "/v1/embeddings", "/v1/completions"],
    input_file_id: str,
    custom_llm_provider: Literal[
        "openai", "azure", "vertex_ai", "bedrock", "hosted_vllm"
    ] = "openai",
    metadata: Optional[Dict[str, str]] = None,
    extra_headers: Optional[Dict[str, str]] = None,
    extra_body: Optional[Dict[str, str]] = None,
    output_expires_after: Optional[Dict[str, Any]] = None,
    **kwargs,
) -> Union[LiteLLMBatch, Coroutine[Any, Any, LiteLLMBatch]]:
    """
    Creates and executes a batch from an uploaded file of request

    LiteLLM Equivalent of POST: https://api.openai.com/v1/batches
    """
    try:
        optional_params = GenericLiteLLMParams(**kwargs)
        litellm_call_id = kwargs.get("litellm_call_id", None)
        proxy_server_request = kwargs.get("proxy_server_request", None)
        model_info = kwargs.get("model_info", None)
        model: Optional[str] = kwargs.get("model", None)
        try:
            if model is not None:
                model, _, _, _ = get_llm_provider(
                    model=model,
                    custom_llm_provider=None,
                )
        except Exception as e:
            verbose_logger.exception(
                f"litellm.batches.main.py::create_batch() - Error inferring custom_llm_provider - {str(e)}"
            )

        _is_async = kwargs.pop("acreate_batch", False) is True
        litellm_params = dict(GenericLiteLLMParams(**kwargs))
        litellm_logging_obj: LiteLLMLoggingObj = cast(
            LiteLLMLoggingObj, kwargs.get("litellm_logging_obj", None)
        )
        ### TIMEOUT LOGIC ###
        timeout = _resolve_timeout(optional_params, kwargs, custom_llm_provider)
        litellm_logging_obj.update_from_kwargs(
            kwargs=kwargs,
            model=model,
            user=None,
            optional_params=optional_params.model_dump(),
            litellm_params={
                "litellm_call_id": litellm_call_id,
                "proxy_server_request": proxy_server_request,
                "model_info": model_info,
                "preset_cache_key": None,
                "stream_response": {},
                **optional_params.model_dump(exclude_unset=True),
            },
            custom_llm_provider=custom_llm_provider,
        )

        _create_batch_request = CreateBatchRequest(
            completion_window=completion_window,
            endpoint=endpoint,
            input_file_id=input_file_id,
            metadata=metadata,
            extra_headers=extra_headers,
            extra_body=extra_body,
        )
        if output_expires_after is not None:
            _create_batch_request["output_expires_after"] = cast(
                FileExpiresAfter, output_expires_after
            )
        if model is not None:
            provider_config = ProviderConfigManager.get_provider_batches_config(
                model=model,
                provider=LlmProviders(custom_llm_provider),
            )
        else:
            provider_config = None
        if provider_config is not None:
            response = base_llm_http_handler.create_batch(
                provider_config=provider_config,
                litellm_params=litellm_params,
                create_batch_data=_create_batch_request,
                headers=extra_headers or {},
                api_base=optional_params.api_base,
                api_key=optional_params.api_key,
                logging_obj=litellm_logging_obj,
                _is_async=_is_async,
                client=(
                    client
                    if client is not None
                    and isinstance(client, (HTTPHandler, AsyncHTTPHandler))
                    else None
                ),
                timeout=timeout,
                model=model,
            )
            return response
        api_base: Optional[str] = None
        if custom_llm_provider in OPENAI_COMPATIBLE_BATCH_AND_FILES_PROVIDERS:
            # for deepinfra/perplexity/anyscale/groq we check in get_llm_provider and pass in the api base from there
            api_base = (
                optional_params.api_base
                or litellm.api_base
                or os.getenv("OPENAI_BASE_URL")
                or os.getenv("OPENAI_API_BASE")
                or "https://api.openai.com/v1"
            )
            organization = (
                optional_params.organization
                or litellm.organization
                or os.getenv("OPENAI_ORGANIZATION", None)
                or None  # default - https://github.com/openai/openai-python/blob/284c1799070c723c6a553337134148a7ab088dd8/openai/util.py#L105
            )
            # set API KEY
            api_key = (
                optional_params.api_key
                or litellm.api_key  # for deepinfra/perplexity/anyscale we check in get_llm_provider and pass in the api key from there
                or litellm.openai_key
                or os.getenv("OPENAI_API_KEY")
            )

            response = openai_batches_instance.create_batch(
                api_base=api_base,
                api_key=api_key,
                organization=organization,
                create_batch_data=_create_batch_request,
                timeout=timeout,
                max_retries=optional_params.max_retries,
                _is_async=_is_async,
            )
        elif custom_llm_provider == "azure":
            api_base = (
                optional_params.api_base
                or litellm.api_base
                or get_secret_str("AZURE_API_BASE")
            )
            api_version = (
                optional_params.api_version
                or litellm.api_version
                or get_secret_str("AZURE_API_VERSION")
            )

            api_key = (
                optional_params.api_key
                or litellm.api_key
                or litellm.azure_key
                or get_secret_str("AZURE_OPENAI_API_KEY")
                or get_secret_str("AZURE_API_KEY")
            )

            extra_body = optional_params.get("extra_body", {})
            if extra_body is not None:
                extra_body.pop("azure_ad_token", None)
            else:
                get_secret_str("AZURE_AD_TOKEN")  # type: ignore

            response = azure_batches_instance.create_batch(
                _is_async=_is_async,
                api_base=api_base,
                api_key=api_key,
                api_version=api_version,
                timeout=timeout,
                max_retries=optional_params.max_retries,
                create_batch_data=_create_batch_request,
                litellm_params=litellm_params,
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

            response = vertex_ai_batches_instance.create_batch(
                _is_async=_is_async,
                api_base=api_base,
                vertex_project=vertex_ai_project,
                vertex_location=vertex_ai_location,
                vertex_credentials=vertex_credentials,
                timeout=timeout,
                max_retries=optional_params.max_retries,
                create_batch_data=_create_batch_request,
            )
        else:
            raise litellm.exceptions.BadRequestError(
                message="LiteLLM doesn't support custom_llm_provider={} for 'create_batch'".format(
                    custom_llm_provider
                ),
                model="n/a",
                llm_provider=custom_llm_provider,
                response=httpx.Response(
                    status_code=400,
                    content="Unsupported provider",
                    request=httpx.Request(method="create_batch", url="https://github.com/BerriAI/litellm"),  # type: ignore
                ),
            )
        return response
    except Exception as e:
        raise e

