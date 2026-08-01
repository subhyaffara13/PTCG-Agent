
def _handle_retrieve_batch_providers_without_provider_config(
    batch_id: str,
    optional_params: GenericLiteLLMParams,
    timeout: Union[float, httpx.Timeout],
    litellm_params: dict,
    _retrieve_batch_request: RetrieveBatchRequest,
    _is_async: bool,
    custom_llm_provider: Literal[
        "openai", "azure", "vertex_ai", "bedrock", "hosted_vllm", "anthropic"
    ] = "openai",
    logging_obj: Optional[Any] = None,
):
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

        response = openai_batches_instance.retrieve_batch(
            _is_async=_is_async,
            retrieve_batch_data=_retrieve_batch_request,
            api_base=api_base,
            api_key=api_key,
            organization=organization,
            timeout=timeout,
            max_retries=optional_params.max_retries,
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

        response = azure_batches_instance.retrieve_batch(
            _is_async=_is_async,
            api_base=api_base,
            api_key=api_key,
            api_version=api_version,
            timeout=timeout,
            max_retries=optional_params.max_retries,
            retrieve_batch_data=_retrieve_batch_request,
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

        response = vertex_ai_batches_instance.retrieve_batch(
            _is_async=_is_async,
            batch_id=batch_id,
            api_base=api_base,
            vertex_project=vertex_ai_project,
            vertex_location=vertex_ai_location,
            vertex_credentials=vertex_credentials,
            timeout=timeout,
            max_retries=optional_params.max_retries,
            logging_obj=logging_obj,
        )
    elif custom_llm_provider == "anthropic":
        api_base = (
            optional_params.api_base
            or litellm.api_base
            or get_secret_str("ANTHROPIC_API_BASE")
            or get_secret_str("ANTHROPIC_BASE_URL")
        )
        api_key = (
            optional_params.api_key
            or litellm.api_key
            or litellm.azure_key
            or get_secret_str("ANTHROPIC_API_KEY")
        )

        response = anthropic_batches_instance.retrieve_batch(
            _is_async=_is_async,
            batch_id=batch_id,
            api_base=api_base,
            api_key=api_key,
            timeout=timeout,
            max_retries=optional_params.max_retries,
        )
    else:
        raise litellm.exceptions.BadRequestError(
            message=(
                "LiteLLM doesn't support custom_llm_provider={} for 'retrieve_batch' without a `model` kwarg. "
                "Supported via this path: 'openai', 'azure', 'vertex_ai', 'anthropic'. "
                "'bedrock' is supported but requires `model` to be passed so the provider config can be loaded."
            ).format(custom_llm_provider),
            model="n/a",
            llm_provider=custom_llm_provider,
            response=httpx.Response(
                status_code=400,
                content="Unsupported provider",
                request=httpx.Request(method="retrieve_batch", url="https://github.com/BerriAI/litellm"),  # type: ignore
            ),
        )
    return response

