
def retrieve_batch(
    batch_id: str,
    custom_llm_provider: Literal[
        "openai", "azure", "vertex_ai", "bedrock", "hosted_vllm", "anthropic"
    ] = "openai",
    metadata: Optional[Dict[str, str]] = None,
    extra_headers: Optional[Dict[str, str]] = None,
    extra_body: Optional[Dict[str, str]] = None,
    **kwargs,
) -> Union[LiteLLMBatch, Coroutine[Any, Any, LiteLLMBatch]]:
    """
    Retrieves a batch.

    LiteLLM Equivalent of GET https://api.openai.com/v1/batches/{batch_id}
    """
    try:
        optional_params = GenericLiteLLMParams(**kwargs)
        litellm_logging_obj: Optional[LiteLLMLoggingObj] = kwargs.get(
            "litellm_logging_obj", None
        )
        ### TIMEOUT LOGIC ###
        timeout = optional_params.timeout or kwargs.get("request_timeout", 600) or 600
        litellm_params = get_litellm_params(
            custom_llm_provider=custom_llm_provider,
            **kwargs,
        )
        if litellm_logging_obj is not None:
            litellm_logging_obj.update_from_kwargs(
                kwargs=kwargs,
                model=None,
                user=None,
                optional_params=optional_params.model_dump(),
                litellm_params=litellm_params,
                custom_llm_provider=custom_llm_provider,
            )

        if (
            timeout is not None
            and isinstance(timeout, httpx.Timeout)
            and supports_httpx_timeout(custom_llm_provider) is False
        ):
            read_timeout = timeout.read or 600
            timeout = read_timeout  # default 10 min timeout
        elif timeout is not None and not isinstance(timeout, httpx.Timeout):
            timeout = float(timeout)  # type: ignore
        elif timeout is None:
            timeout = 600.0

        _retrieve_batch_request = RetrieveBatchRequest(
            batch_id=batch_id,
            extra_headers=extra_headers,
            extra_body=extra_body,
        )

        _is_async = kwargs.pop("aretrieve_batch", False) is True
        client = kwargs.get("client", None)

        # Bedrock has two distinct ARN families that need different APIs:
        #   * async-invoke ARNs       (Twelve Labs Marengo embeddings)        -> bedrock-runtime data plane
        #   * model-invocation-job ARNs (CreateModelInvocationJob batch)      -> bedrock control plane
        # They live on different AWS service endpoints and can't share a handler.
        # ARN shapes:
        #   arn:aws(-[^:]+)?:bedrock:<region>:<account>:async-invoke/<id>
        #   arn:aws(-[^:]+)?:bedrock:<region>:<account>:model-invocation-job/<id>
        if batch_id.startswith("arn:aws") and ":bedrock:" in batch_id:
            if ":async-invoke/" in batch_id:
                # Remove aws_region_name from kwargs to avoid duplicate parameter
                async_kwargs = kwargs.copy()
                async_kwargs.pop("aws_region_name", None)

                return BedrockBatchesHandler._handle_async_invoke_status(
                    batch_id=batch_id,
                    aws_region_name=kwargs.get("aws_region_name", "us-east-1"),
                    logging_obj=litellm_logging_obj,
                    **async_kwargs,
                )
            if ":model-invocation-job/" in batch_id:
                mij_kwargs = kwargs.copy()
                mij_kwargs.pop("aws_region_name", None)

                return BedrockBatchesHandler._handle_model_invocation_job_status(
                    batch_id=batch_id,
                    aws_region_name=kwargs.get("aws_region_name"),
                    logging_obj=litellm_logging_obj,
                    **mij_kwargs,
                )

        # Try to use provider config first (for providers like bedrock)
        model: Optional[str] = kwargs.get("model", None)
        if model is not None:
            provider_config = ProviderConfigManager.get_provider_batches_config(
                model=model,
                provider=LlmProviders(custom_llm_provider),
            )
        else:
            provider_config = None

        if provider_config is not None:
            response = base_llm_http_handler.retrieve_batch(
                batch_id=batch_id,
                provider_config=provider_config,
                litellm_params=litellm_params,
                headers=extra_headers or {},
                api_base=optional_params.api_base,
                api_key=optional_params.api_key,
                logging_obj=litellm_logging_obj
                or LiteLLMLoggingObj(
                    model=model or f"{custom_llm_provider}/unknown",
                    messages=[],
                    stream=False,
                    call_type="batch_retrieve",
                    start_time=None,
                    litellm_call_id="batch_retrieve_" + batch_id,
                    function_id="batch_retrieve",
                ),
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

        #########################################################
        # Handle providers without provider config
        #########################################################
        return _handle_retrieve_batch_providers_without_provider_config(
            batch_id=batch_id,
            custom_llm_provider=custom_llm_provider,
            optional_params=optional_params,
            litellm_params=litellm_params,
            _retrieve_batch_request=_retrieve_batch_request,
            _is_async=_is_async,
            timeout=timeout,
            logging_obj=litellm_logging_obj,
        )

    except Exception as e:
        raise e

