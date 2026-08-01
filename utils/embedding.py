
def embedding(
    model,
    input=[],
    # Optional params
    dimensions: Optional[int] = None,
    encoding_format: Optional[str] = None,
    timeout=600,  # default to 10 minutes
    # set api_base, api_version, api_key
    api_base: Optional[str] = None,
    api_version: Optional[str] = None,
    api_key: Optional[str] = None,
    api_type: Optional[str] = None,
    caching: bool = False,
    user: Optional[str] = None,
    custom_llm_provider=None,
    litellm_call_id=None,
    logger_fn=None,
    *,
    aembedding: Literal[True],
    **kwargs,
) -> Coroutine[Any, Any, EmbeddingResponse]: 
    ...


def embedding(
    model,
    input=[],
    # Optional params
    dimensions: Optional[int] = None,
    encoding_format: Optional[str] = None,
    timeout=600,  # default to 10 minutes
    # set api_base, api_version, api_key
    api_base: Optional[str] = None,
    api_version: Optional[str] = None,
    api_key: Optional[str] = None,
    api_type: Optional[str] = None,
    caching: bool = False,
    user: Optional[str] = None,
    custom_llm_provider=None,
    litellm_call_id=None,
    logger_fn=None,
    *,
    aembedding: Literal[False] = False,
    **kwargs,
) -> EmbeddingResponse: 
    ...


def embedding(
    model,
    input=[],
    # Optional params
    dimensions: Optional[int] = None,
    encoding_format: Optional[str] = None,
    timeout=600,  # default to 10 minutes
    # set api_base, api_version, api_key
    api_base: Optional[str] = None,
    api_version: Optional[str] = None,
    api_key: Optional[str] = None,
    api_type: Optional[str] = None,
    caching: bool = False,
    user: Optional[str] = None,
    custom_llm_provider=None,
    litellm_call_id=None,
    logger_fn=None,
    **kwargs,
) -> Union[EmbeddingResponse, Coroutine[Any, Any, EmbeddingResponse]]:
    """
    Embedding function that calls an API to generate embeddings for the given input.

    Parameters:
    - model: The embedding model to use.
    - input: The input for which embeddings are to be generated.
    - encoding_format: Optional[str] The format to return the embeddings in. Can be either `float` or `base64`
    - dimensions: The number of dimensions the resulting output embeddings should have. Only supported in text-embedding-3 and later models.
    - timeout: The timeout value for the API call, default 10 mins
    - litellm_call_id: The call ID for litellm logging.
    - litellm_logging_obj: The litellm logging object.
    - logger_fn: The logger function.
    - api_base: Optional. The base URL for the API.
    - api_version: Optional. The version of the API.
    - api_key: Optional. The API key to use.
    - api_type: Optional. The type of the API.
    - caching: A boolean indicating whether to enable caching.
    - custom_llm_provider: The custom llm provider.

    Returns:
    - response: The response received from the API call.

    Raises:
    - exception_type: If an exception occurs during the API call.
    """
    azure = kwargs.get("azure", None)
    client = kwargs.pop("client", None)
    shared_session = kwargs.get("shared_session", None)
    max_retries = kwargs.get("max_retries", None)
    litellm_logging_obj: LiteLLMLoggingObj = kwargs.get("litellm_logging_obj")  # type: ignore
    mock_response: Optional[List[float]] = kwargs.get("mock_response", None)  # type: ignore
    azure_ad_token_provider = kwargs.get("azure_ad_token_provider", None)
    aembedding: Optional[bool] = kwargs.get("aembedding", None)
    extra_headers = kwargs.get("extra_headers", None)
    headers = kwargs.get("headers", None) or extra_headers
    if headers is None:
        headers = {}
    if extra_headers is not None:
        headers.update(extra_headers)
    # Inject proxy auth headers if configured
    if litellm.proxy_auth is not None:
        try:
            proxy_headers = litellm.proxy_auth.get_auth_headers()
            headers.update(proxy_headers)
        except Exception as e:
            verbose_logger.warning(f"Failed to get proxy auth headers: {e}")
    ### CUSTOM MODEL COST ###
    input_cost_per_token = kwargs.get("input_cost_per_token", None)
    output_cost_per_token = kwargs.get("output_cost_per_token", None)
    input_cost_per_second = kwargs.get("input_cost_per_second", None)
    openai_params = [
        "user",
        "dimensions",
        "request_timeout",
        "api_base",
        "api_version",
        "api_key",
        "deployment_id",
        "organization",
        "base_url",
        "default_headers",
        "timeout",
        "max_retries",
        "encoding_format",
    ]
    litellm_params = [
        "aembedding",
        "extra_headers",
    ] + all_litellm_params

    default_params = openai_params + litellm_params
    non_default_params = {
        k: v for k, v in kwargs.items() if k not in default_params
    }  # model-specific params - pass them straight to the model/provider

    model, custom_llm_provider, dynamic_api_key, api_base = get_llm_provider(
        model=model,
        custom_llm_provider=custom_llm_provider,
        api_base=api_base,
        api_key=api_key,
    )

    if dynamic_api_key is not None:
        api_key = dynamic_api_key

    allowed_openai_params: Optional[List[str]] = kwargs.get(
        "allowed_openai_params", None
    )
    optional_params = get_optional_params_embeddings(
        model=model,
        user=user,
        dimensions=dimensions,
        encoding_format=encoding_format,
        custom_llm_provider=custom_llm_provider,
        allowed_openai_params=allowed_openai_params,
        **non_default_params,
    )

    ### REGISTER CUSTOM MODEL PRICING -- IF GIVEN ###
    if (
        input_cost_per_token is not None and output_cost_per_token is not None
    ) or input_cost_per_second is not None:
        litellm.register_model(
            {
                f"{custom_llm_provider}/{model}": _build_custom_pricing_entry(
                    custom_llm_provider=custom_llm_provider,
                    kwargs=kwargs,
                    model_info=kwargs.get("model_info"),
                )
            }
        )

    litellm_params_dict = get_litellm_params(**kwargs)

    logging: LiteLLMLoggingObj = litellm_logging_obj  # type: ignore
    logging.update_environment_variables(
        model=model,
        user=user,
        optional_params=optional_params,
        litellm_params=litellm_params_dict,
        custom_llm_provider=custom_llm_provider,
    )

    if mock_response is not None:
        return mock_embedding(model=model, mock_response=mock_response)
    try:
        response: Optional[
            Union[EmbeddingResponse, Coroutine[Any, Any, EmbeddingResponse]]
        ] = None

        if azure is True or custom_llm_provider == "azure":
            # azure configs

            api_base = api_base or litellm.api_base or get_secret_str("AZURE_API_BASE")

            api_version = (
                api_version
                or litellm.api_version
                or get_secret_str("AZURE_API_VERSION")
                or litellm.AZURE_DEFAULT_API_VERSION
            )

            azure_ad_token = optional_params.pop(
                "azure_ad_token", None
            ) or get_secret_str("AZURE_AD_TOKEN")

            api_key = (
                api_key
                or litellm.api_key
                or litellm.azure_key
                or get_secret_str("AZURE_API_KEY")
            )

            if api_base is None:
                raise ValueError(
                    "No API Base provided for Azure OpenAI LLM provider. Set 'AZURE_API_BASE' in .env"
                )

            ## EMBEDDING CALL
            response = azure_chat_completions.embedding(
                model=model,
                input=input,
                api_base=api_base,
                api_key=api_key,
                api_version=api_version,
                azure_ad_token=azure_ad_token,
                azure_ad_token_provider=azure_ad_token_provider,
                logging_obj=logging,
                timeout=timeout,
                model_response=EmbeddingResponse(),
                optional_params=optional_params,
                client=client,
                aembedding=aembedding,
                max_retries=max_retries,
                headers=headers or extra_headers,
                litellm_params=litellm_params_dict,
            )
        elif custom_llm_provider == "github_copilot":
            api_key = api_key or litellm.api_key
            response = base_llm_http_handler.embedding(
                model=model,
                input=input,
                custom_llm_provider=custom_llm_provider,
                api_base=api_base,
                api_key=api_key,
                logging_obj=logging,
                timeout=timeout,
                model_response=EmbeddingResponse(),
                optional_params=optional_params,
                client=client,
                aembedding=aembedding,
                litellm_params=litellm_params_dict,
            )
        elif (
            custom_llm_provider == "openai"
            or custom_llm_provider == "together_ai"
            or custom_llm_provider == "nvidia_nim"
            or custom_llm_provider == "litellm_proxy"
            or (
                model in litellm.open_ai_embedding_models
                and custom_llm_provider is None
            )
        ):
            api_base = (
                api_base
                or litellm.api_base
                or get_secret_str("OPENAI_BASE_URL")
                or get_secret_str("OPENAI_API_BASE")
                or "https://api.openai.com/v1"
            )
            openai.organization = (
                litellm.organization
                or get_secret_str("OPENAI_ORGANIZATION")
                or None  # default - https://github.com/openai/openai-python/blob/284c1799070c723c6a553337134148a7ab088dd8/openai/util.py#L105
            )
            # set API KEY
            api_key = (
                api_key
                or litellm.api_key
                or litellm.openai_key
                or get_secret_str("OPENAI_API_KEY")
            )

            if headers is not None and headers != {}:
                optional_params["extra_headers"] = headers

            if encoding_format is not None:
                optional_params["encoding_format"] = encoding_format
            else:
                env_fmt = get_secret_str("LITELLM_DEFAULT_EMBEDDING_ENCODING_FORMAT")
                if env_fmt is not None and env_fmt.strip().lower() == "none":
                    optional_params.pop("encoding_format", None)
                else:
                    _default_fmt = (
                        optional_params.get("encoding_format") or env_fmt or "float"
                    )
                    if _default_fmt.strip().lower() == "none":
                        optional_params.pop("encoding_format", None)
                    else:
                        optional_params["encoding_format"] = _default_fmt

            api_version = None

            ## EMBEDDING CALL
            response = openai_chat_completions.embedding(
                model=model,
                input=input,
                api_base=api_base,
                api_key=api_key,
                logging_obj=logging,
                timeout=timeout,
                model_response=EmbeddingResponse(),
                optional_params=optional_params,
                client=client,
                aembedding=aembedding,
                max_retries=max_retries,
                shared_session=shared_session,
            )
        elif custom_llm_provider == "databricks":
            api_base = api_base or litellm.api_base or get_secret("DATABRICKS_API_BASE")  # type: ignore

            # set API KEY
            api_key = (
                api_key
                or litellm.api_key
                or litellm.databricks_key
                or get_secret("DATABRICKS_API_KEY")
            )  # type: ignore

            ## EMBEDDING CALL
            response = databricks_embedding.embedding(
                model=model,
                input=input,
                api_base=api_base,
                api_key=api_key,
                logging_obj=logging,
                timeout=timeout,
                model_response=EmbeddingResponse(),
                optional_params=optional_params,
                client=client,
                aembedding=aembedding,
            )
        elif custom_llm_provider == "hosted_vllm":
            api_base = (
                api_base or litellm.api_base or get_secret_str("HOSTED_VLLM_API_BASE")
            )

            # set API KEY
            if api_key is None:
                api_key = litellm.api_key or get_secret_str("HOSTED_VLLM_API_KEY")

            response = base_llm_http_handler.embedding(
                model=model,
                input=input,
                custom_llm_provider=custom_llm_provider,
                api_base=api_base,
                api_key=api_key,
                logging_obj=logging,
                timeout=timeout,
                model_response=EmbeddingResponse(),
                optional_params=optional_params,
                client=client,
                aembedding=aembedding,
                litellm_params=litellm_params_dict,
                headers=headers or {},
            )
        elif (
            custom_llm_provider == "openai_like"
            or custom_llm_provider == "llamafile"
            or custom_llm_provider == "lm_studio"
        ):
            api_base = (
                api_base or litellm.api_base or get_secret_str("OPENAI_LIKE_API_BASE")
            )

            # set API KEY
            if api_key is None:
                api_key = (
                    api_key
                    or litellm.api_key
                    or litellm.openai_like_key
                    or get_secret_str("OPENAI_LIKE_API_KEY")
                )

            if headers is not None and headers != {}:
                optional_params["extra_headers"] = headers

            ## EMBEDDING CALL
            response = openai_like_embedding.embedding(
                model=model,
                input=input,
                api_base=api_base,
                api_key=api_key,
                logging_obj=logging,
                timeout=timeout,
                model_response=EmbeddingResponse(),
                optional_params=optional_params,
                client=client,
                aembedding=aembedding,
            )
        elif custom_llm_provider == "oci":
            if headers is None:
                headers = {}
            response = base_llm_http_handler.embedding(
                model=model,
                input=input,
                custom_llm_provider=custom_llm_provider,
                api_base=api_base,
                api_key=api_key,
                logging_obj=logging,
                timeout=timeout,
                model_response=EmbeddingResponse(),
                optional_params=optional_params,
                client=client,
                aembedding=aembedding,
                litellm_params=litellm_params_dict,
                headers=headers,
            )
        elif custom_llm_provider == "cohere" or custom_llm_provider == "cohere_chat":
            cohere_key = (
                api_key
                or litellm.cohere_key
                or get_secret_str("COHERE_API_KEY")
                or get_secret_str("CO_API_KEY")
                or litellm.api_key
            )

            # Use the merged headers variable (already merged at the top of the function)
            # Don't overwrite it with just extra_headers
            if headers is None:
                headers = {}

            response = base_llm_http_handler.embedding(
                model=model,
                input=input,
                custom_llm_provider=custom_llm_provider,
                api_base=api_base,
                api_key=cohere_key,
                logging_obj=logging,
                timeout=timeout,
                model_response=EmbeddingResponse(),
                optional_params=optional_params,
                client=client,
                aembedding=aembedding,
                litellm_params=litellm_params_dict,
                headers=headers,
            )
        elif custom_llm_provider == "openrouter":
            api_base = (
                api_base
                or litellm.api_base
                or get_secret_str("OPENROUTER_API_BASE")
                or "https://openrouter.ai/api/v1"
            )

            api_key = (
                api_key
                or litellm.api_key
                or litellm.openrouter_key
                or get_secret_str("OPENROUTER_API_KEY")
                or get_secret_str("OR_API_KEY")
            )

            openrouter_site_url = get_secret("OR_SITE_URL") or "https://litellm.ai"
            openrouter_app_name = get_secret("OR_APP_NAME") or "liteLLM"

            openrouter_headers = {
                "HTTP-Referer": openrouter_site_url,
                "X-Title": openrouter_app_name,
            }

            _headers = headers or litellm.headers
            if _headers:
                openrouter_headers.update(_headers)

            headers = openrouter_headers

            response = base_llm_http_handler.embedding(
                model=model,
                input=input,
                custom_llm_provider=custom_llm_provider,
                api_base=api_base,
                api_key=api_key,
                logging_obj=logging,
                timeout=timeout,
                model_response=EmbeddingResponse(),
                optional_params=optional_params,
                client=client,
                aembedding=aembedding,
                litellm_params=litellm_params_dict,
                headers=headers,
            )
        elif custom_llm_provider == "vercel_ai_gateway":
            api_base = (
                api_base
                or litellm.api_base
                or get_secret_str("VERCEL_AI_GATEWAY_API_BASE")
                or "https://ai-gateway.vercel.sh/v1"
            )

            api_key = (
                api_key
                or litellm.api_key
                or get_secret_str("VERCEL_AI_GATEWAY_API_KEY")
                or get_secret_str("VERCEL_OIDC_TOKEN")
            )

            response = base_llm_http_handler.embedding(
                model=model,
                input=input,
                custom_llm_provider=custom_llm_provider,
                api_base=api_base,
                api_key=api_key,
                logging_obj=logging,
                timeout=timeout,
                model_response=EmbeddingResponse(),
                optional_params=optional_params,
                client=client,
                aembedding=aembedding,
                litellm_params=litellm_params_dict,
                headers=headers,
            )
        elif custom_llm_provider == "huggingface":
            api_key = (
                api_key
                or litellm.huggingface_key
                or get_secret("HUGGINGFACE_API_KEY")
                or litellm.api_key
            )  # type: ignore
            response = huggingface_embed.embedding(
                model=model,
                input=input,
                encoding=_get_encoding(),  # type: ignore
                api_key=api_key,
                api_base=api_base,
                logging_obj=logging,
                model_response=EmbeddingResponse(),
                optional_params=optional_params,
                client=client,
                aembedding=aembedding,
                litellm_params=litellm_params_dict,
                headers=headers,
            )
        elif custom_llm_provider == "bedrock":
            if isinstance(input, str):
                transformed_input = [input]
            else:
                transformed_input = input
            response = bedrock_embedding.embeddings(
                model=model,
                input=transformed_input,
                encoding=_get_encoding(),
                logging_obj=logging,
                optional_params=optional_params,
                model_response=EmbeddingResponse(),
                client=client,
                timeout=timeout,
                aembedding=aembedding,
                litellm_params={},
                api_base=api_base,
                print_verbose=print_verbose,
                extra_headers=headers,
                api_key=api_key,
            )
        elif custom_llm_provider == "triton":
            if api_base is None:
                raise ValueError(
                    "api_base is required for triton. Please pass `api_base`"
                )
            response = base_llm_http_handler.embedding(
                model=model,
                input=input,
                custom_llm_provider=custom_llm_provider,
                api_base=api_base,
                api_key=api_key,
                logging_obj=logging,
                timeout=timeout,
                model_response=EmbeddingResponse(),
                optional_params=optional_params,
                client=client,
                aembedding=aembedding,
                litellm_params={},
            )
        elif custom_llm_provider == "gemini":
            gemini_api_key = api_key or get_api_key_from_env() or litellm.api_key

            api_base = api_base or litellm.api_base or get_secret_str("GEMINI_API_BASE")

            response = google_batch_embeddings.batch_embeddings(  # type: ignore
                model=model,
                input=input,
                encoding=_get_encoding(),
                logging_obj=logging,
                optional_params=optional_params,
                model_response=EmbeddingResponse(),
                vertex_project=None,
                vertex_location=None,
                vertex_credentials=None,
                aembedding=aembedding,
                print_verbose=print_verbose,
                custom_llm_provider="gemini",
                api_key=gemini_api_key,
                api_base=api_base,
                client=client,
                extra_headers=headers,
            )

        elif custom_llm_provider == "vertex_ai":
            vertex_ai_project = (
                optional_params.pop("vertex_project", None)
                or optional_params.pop("vertex_ai_project", None)
                or litellm.vertex_project
                or get_secret_str("VERTEXAI_PROJECT")
                or get_secret_str("VERTEX_PROJECT")
            )
            vertex_ai_location = (
                optional_params.pop("vertex_location", None)
                or optional_params.pop("vertex_ai_location", None)
                or litellm.vertex_location
                or get_secret_str("VERTEXAI_LOCATION")
                or get_secret_str("VERTEX_LOCATION")
            )
            vertex_credentials = (
                optional_params.pop("vertex_credentials", None)
                or optional_params.pop("vertex_ai_credentials", None)
                or get_secret_str("VERTEXAI_CREDENTIALS")
                or get_secret_str("VERTEX_CREDENTIALS")
            )

            api_base = (
                api_base
                or litellm.api_base
                or get_secret_str("VERTEXAI_API_BASE")
                or get_secret_str("VERTEX_API_BASE")
            )

            try:
                model_info = get_model_info(
                    model=model, custom_llm_provider="vertex_ai"
                )
                uses_embed_content = model_info.get("uses_embed_content", False)
            except Exception:
                uses_embed_content = False

            if uses_embed_content:
                response = google_batch_embeddings.batch_embeddings(  # type: ignore
                    model=model,
                    input=input,
                    encoding=_get_encoding(),
                    logging_obj=logging,
                    optional_params=optional_params,
                    model_response=EmbeddingResponse(),
                    vertex_project=vertex_ai_project,
                    vertex_location=vertex_ai_location,
                    vertex_credentials=vertex_credentials,
                    aembedding=aembedding,
                    print_verbose=print_verbose,
                    custom_llm_provider="vertex_ai",
                    api_key=None,
                    api_base=api_base,
                    client=client,
                    extra_headers=headers,
                )
            elif (
                "image" in optional_params
                or "video" in optional_params
                or model
                in vertex_multimodal_embedding.SUPPORTED_MULTIMODAL_EMBEDDING_MODELS
            ):
                response = vertex_multimodal_embedding.multimodal_embedding(
                    model=model,
                    input=input,
                    encoding=_get_encoding(),
                    logging_obj=logging,
                    optional_params=optional_params,
                    litellm_params=litellm_params_dict,
                    model_response=EmbeddingResponse(),
                    vertex_project=vertex_ai_project,
                    vertex_location=vertex_ai_location,
                    vertex_credentials=vertex_credentials,
                    aembedding=aembedding,
                    print_verbose=print_verbose,
                    custom_llm_provider="vertex_ai",
                    client=client,
                    api_base=api_base,
                )
            else:
                response = vertex_embedding.embedding(
                    model=model,
                    input=input,
                    encoding=_get_encoding(),
                    logging_obj=logging,
                    optional_params=optional_params,
                    model_response=EmbeddingResponse(),
                    vertex_project=vertex_ai_project,
                    vertex_location=vertex_ai_location,
                    vertex_credentials=vertex_credentials,
                    custom_llm_provider="vertex_ai",
                    timeout=timeout,
                    aembedding=aembedding,
                    print_verbose=print_verbose,
                    api_key=api_key,
                    api_base=api_base,
                    client=client,
                    litellm_params=litellm_params_dict,
                )
        elif custom_llm_provider == "oobabooga":
            response = oobabooga.embedding(
                model=model,
                input=input,
                encoding=_get_encoding(),
                api_base=api_base,
                logging_obj=logging,
                optional_params=optional_params,
                model_response=EmbeddingResponse(),
                api_key=api_key,
            )
        elif custom_llm_provider == "ollama":
            api_base = (
                litellm.api_base
                or api_base
                or get_secret_str("OLLAMA_API_BASE")
                or "http://localhost:11434"
            )  # type: ignore

            if isinstance(input, str):
                input = [input]
            if not all(isinstance(item, str) for item in input):
                raise litellm.BadRequestError(
                    message=f"Invalid input for ollama embeddings. input={input}",
                    model=model,  # type: ignore
                    llm_provider="ollama",  # type: ignore
                )
            ollama_embeddings_fn = (
                ollama.ollama_aembeddings
                if aembedding is True
                else ollama.ollama_embeddings
            )
            response = ollama_embeddings_fn(  # type: ignore
                api_base=api_base,
                model=model,
                prompts=input,
                encoding=_get_encoding(),
                logging_obj=logging,
                optional_params=optional_params,
                model_response=EmbeddingResponse(),
            )
        elif custom_llm_provider == "sagemaker":
            response = sagemaker_llm.embedding(
                model=model,
                input=input,
                encoding=_get_encoding(),
                logging_obj=logging,
                optional_params=optional_params,
                model_response=EmbeddingResponse(),
                print_verbose=print_verbose,
            )
        elif custom_llm_provider == "mistral":
            api_key = api_key or litellm.api_key or get_secret_str("MISTRAL_API_KEY")
            response = openai_chat_completions.embedding(
                model=model,
                input=input,
                api_base=api_base,
                api_key=api_key,
                logging_obj=logging,
                timeout=timeout,
                model_response=EmbeddingResponse(),
                optional_params=optional_params,
                client=client,
                aembedding=aembedding,
            )
        elif custom_llm_provider == "fireworks_ai":
            api_key = (
                api_key or litellm.api_key or get_secret_str("FIREWORKS_AI_API_KEY")
            )
            response = openai_chat_completions.embedding(
                model=model,
                input=input,
                api_base=api_base,
                api_key=api_key,
                logging_obj=logging,
                timeout=timeout,
                model_response=EmbeddingResponse(),
                optional_params=optional_params,
                client=client,
                aembedding=aembedding,
            )
        elif custom_llm_provider == "nebius":
            api_key = api_key or litellm.api_key or get_secret_str("NEBIUS_API_KEY")
            api_base = (
                api_base
                or litellm.api_base
                or get_secret_str("NEBIUS_API_BASE")
                or "api.studio.nebius.ai/v1"
            )

            response = openai_chat_completions.embedding(
                model=model,
                input=input,
                api_base=api_base,
                api_key=api_key,
                logging_obj=logging,
                timeout=timeout,
                model_response=EmbeddingResponse(),
                optional_params=optional_params,
                client=client,
                aembedding=aembedding,
            )
        elif custom_llm_provider == "wandb":
            api_key = api_key or litellm.api_key or get_secret_str("WANDB_API_KEY")
            api_base = (
                api_base
                or litellm.api_base
                or get_secret_str("WANDB_API_BASE")
                or "https://api.inference.wandb.ai/v1"
            )

            response = openai_chat_completions.embedding(
                model=model,
                input=input,
                api_base=api_base,
                api_key=api_key,
                logging_obj=logging,
                timeout=timeout,
                model_response=EmbeddingResponse(),
                optional_params=optional_params,
                client=client,
                aembedding=aembedding,
            )
        elif custom_llm_provider == "sambanova":
            api_key = api_key or litellm.api_key or get_secret_str("SAMBANOVA_API_KEY")
            api_base = (
                api_base
                or litellm.api_base
                or get_secret_str("SAMBANOVA_API_BASE")
                or "https://api.sambanova.ai/v1"
            )
            response = base_llm_http_handler.embedding(
                model=model,
                input=input,
                custom_llm_provider=custom_llm_provider,
                api_base=api_base,
                api_key=api_key,
                logging_obj=logging,
                timeout=timeout,
                model_response=EmbeddingResponse(),
                optional_params=optional_params,
                client=client,
                aembedding=aembedding,
                litellm_params={},
            )
        elif custom_llm_provider == "voyage":
            response = base_llm_http_handler.embedding(
                model=model,
                input=input,
                custom_llm_provider=custom_llm_provider,
                api_base=api_base,
                api_key=api_key,
                logging_obj=logging,
                timeout=timeout,
                model_response=EmbeddingResponse(),
                optional_params=optional_params,
                client=client,
                aembedding=aembedding,
                litellm_params={},
            )
        elif custom_llm_provider == "infinity":
            response = base_llm_http_handler.embedding(
                model=model,
                input=input,
                custom_llm_provider=custom_llm_provider,
                api_base=api_base,
                api_key=api_key,
                logging_obj=logging,
                timeout=timeout,
                model_response=EmbeddingResponse(),
                optional_params=optional_params,
                client=client,
                aembedding=aembedding,
                litellm_params={},
            )
        elif custom_llm_provider == "watsonx":
            credentials = IBMWatsonXMixin.get_watsonx_credentials(
                optional_params=optional_params, api_key=api_key, api_base=api_base
            )

            api_key = credentials["api_key"]
            api_base = credentials["api_base"]

            if "token" in credentials:
                optional_params["token"] = credentials["token"]

            response = base_llm_http_handler.embedding(
                model=model,
                input=input,
                custom_llm_provider=custom_llm_provider,
                api_base=api_base,
                api_key=api_key,
                logging_obj=logging,
                timeout=timeout,
                model_response=EmbeddingResponse(),
                optional_params=optional_params,
                litellm_params={},
                client=client,
                aembedding=aembedding,
            )
        elif custom_llm_provider == "xinference":
            api_key = (
                api_key
                or litellm.api_key
                or get_secret_str("XINFERENCE_API_KEY")
                or "stub-xinference-key"
            )  # xinference does not need an api key, pass a stub key if user did not set one
            api_base = (
                api_base
                or litellm.api_base
                or get_secret_str("XINFERENCE_API_BASE")
                or "http://127.0.0.1:9997/v1"
            )
            response = openai_chat_completions.embedding(
                model=model,
                input=input,
                api_base=api_base,
                api_key=api_key,
                logging_obj=logging,
                timeout=timeout,
                model_response=EmbeddingResponse(),
                optional_params=optional_params,
                client=client,
                aembedding=aembedding,
            )
        elif custom_llm_provider == "sap":
            response = base_llm_http_handler.embedding(
                model=model,
                input=input,
                custom_llm_provider=custom_llm_provider,
                api_base=api_base,
                api_key=api_key,
                logging_obj=logging,
                timeout=timeout,
                model_response=EmbeddingResponse(),
                optional_params=optional_params,
                litellm_params={},
                client=client,
                aembedding=aembedding,
            )
        elif custom_llm_provider == "azure_ai":
            api_base = (
                api_base  # for deepinfra/perplexity/anyscale/groq/friendliai we check in get_llm_provider and pass in the api base from there
                or litellm.api_base
                or get_secret_str("AZURE_AI_API_BASE")
            )
            # set API KEY
            api_key = (
                api_key
                or litellm.api_key  # for deepinfra/perplexity/anyscale/friendliai we check in get_llm_provider and pass in the api key from there
                or litellm.openai_key
                or get_secret_str("AZURE_AI_API_KEY")
            )

            ## EMBEDDING CALL
            response = azure_ai_embedding.embedding(
                model=model,
                input=input,
                api_base=api_base,
                api_key=api_key,
                logging_obj=logging,
                timeout=timeout,
                model_response=EmbeddingResponse(),
                optional_params=optional_params,
                client=client,
                aembedding=aembedding,
            )
        elif custom_llm_provider == "jina_ai":
            if isinstance(input, str):
                transformed_input = [input]
            else:
                transformed_input = input
            response = base_llm_http_handler.embedding(
                model=model,
                input=transformed_input,
                custom_llm_provider=custom_llm_provider,
                api_base=api_base,
                api_key=api_key,
                logging_obj=logging,
                timeout=timeout,
                model_response=EmbeddingResponse(),
                optional_params=optional_params,
                litellm_params={},
                client=client,
                aembedding=aembedding,
            )
        elif custom_llm_provider == "volcengine":
            volcengine_key = (
                api_key
                or litellm.api_key
                or get_secret_str("ARK_API_KEY")
                or get_secret_str("VOLCENGINE_API_KEY")
            )
            if volcengine_key is None:
                raise ValueError(
                    "Missing API key for Volcengine. Set ARK_API_KEY or VOLCENGINE_API_KEY environment variable or pass api_key parameter."
                )
            if extra_headers is not None and isinstance(extra_headers, dict):
                headers = extra_headers
            else:
                headers = {}
            response = base_llm_http_handler.embedding(
                model=model,
                input=input,
                timeout=timeout,
                custom_llm_provider=custom_llm_provider,
                logging_obj=logging,
                api_base=api_base,
                optional_params=optional_params,
                litellm_params={},
                model_response=EmbeddingResponse(),
                api_key=volcengine_key,
                client=client,
                aembedding=aembedding,
                headers=headers,
            )
        elif custom_llm_provider == "dashscope":
            dashscope_key = (
                api_key or litellm.api_key or get_secret_str("DASHSCOPE_API_KEY")
            )
            if dashscope_key is None:
                raise ValueError(
                    "Missing API key for DashScope. Set DASHSCOPE_API_KEY environment variable or pass api_key parameter."
                )
            if extra_headers is not None and isinstance(extra_headers, dict):
                headers = extra_headers
            else:
                headers = {}
            response = base_llm_http_handler.embedding(
                model=model,
                input=input,
                timeout=timeout,
                custom_llm_provider=custom_llm_provider,
                logging_obj=logging,
                api_base=api_base,
                optional_params=optional_params,
                litellm_params={},
                model_response=EmbeddingResponse(),
                api_key=dashscope_key,
                client=client,
                aembedding=aembedding,
                headers=headers,
            )
        elif custom_llm_provider == "ovhcloud":
            api_key = api_key or litellm.api_key or get_secret_str("OVHCLOUD_API_KEY")
            api_base = (
                api_base
                or litellm.api_base
                or get_secret_str("OVHCLOUD_API_BASE")
                or "https://oai.endpoints.kepler.ai.cloud.ovh.net/v1"
            )
            response = base_llm_http_handler.embedding(
                model=model,
                input=input,
                custom_llm_provider=custom_llm_provider,
                api_base=api_base,
                api_key=api_key,
                logging_obj=logging,
                timeout=timeout,
                model_response=EmbeddingResponse(),
                optional_params=optional_params,
                client=client,
                aembedding=aembedding,
                litellm_params={},
            )
        elif custom_llm_provider == "cometapi":
            api_key = (
                api_key
                or litellm.cometapi_key
                or get_secret_str("COMETAPI_KEY")
                or litellm.api_key
            )
            api_base = (
                api_base
                or litellm.api_base
                or get_secret_str("COMETAPI_API_BASE")
                or "https://api.cometapi.com/v1"
            )
            response = base_llm_http_handler.embedding(
                model=model,
                input=input,
                custom_llm_provider=custom_llm_provider,
                api_base=api_base,
                api_key=api_key,
                logging_obj=logging,
                timeout=timeout,
                model_response=EmbeddingResponse(),
                optional_params=optional_params,
                client=client,
                aembedding=aembedding,
                litellm_params={},
            )
        elif custom_llm_provider in litellm._custom_providers:
            custom_handler: Optional[CustomLLM] = None
            for item in litellm.custom_provider_map:
                if item["provider"] == custom_llm_provider:
                    custom_handler = item["custom_handler"]

            if custom_handler is None:
                raise LiteLLMUnknownProvider(
                    model=model, custom_llm_provider=custom_llm_provider
                )

            handler_fn = (
                custom_handler.embedding
                if not aembedding
                else custom_handler.aembedding
            )

            response = handler_fn(
                model=model,
                input=input,
                logging_obj=logging,
                api_base=api_base,
                api_key=api_key,
                timeout=timeout,
                optional_params=optional_params,
                model_response=EmbeddingResponse(),
                print_verbose=print_verbose,
                litellm_params=litellm_params_dict,
            )
        elif custom_llm_provider == "snowflake":
            api_key = api_key or get_secret_str("SNOWFLAKE_JWT")
            response = base_llm_http_handler.embedding(
                model=model,
                input=input,
                custom_llm_provider=custom_llm_provider,
                api_base=api_base,
                api_key=api_key,
                logging_obj=logging,
                timeout=timeout,
                model_response=EmbeddingResponse(),
                optional_params=optional_params,
                client=client,
                aembedding=aembedding,
                litellm_params={},
            )
        elif custom_llm_provider == "gigachat":
            api_key = (
                api_key
                or litellm.api_key
                or litellm.gigachat_key
                or get_secret_str("GIGACHAT_CREDENTIALS")
                or get_secret_str("GIGACHAT_API_KEY")
            )
            response = base_llm_http_handler.embedding(
                model=model,
                input=input,
                custom_llm_provider=custom_llm_provider,
                api_base=api_base,
                api_key=api_key,
                logging_obj=logging,
                timeout=timeout,
                model_response=EmbeddingResponse(),
                optional_params=optional_params,
                client=client,
                aembedding=aembedding,
                litellm_params={"ssl_verify": kwargs.get("ssl_verify", None)},
            )
        elif custom_llm_provider == "perplexity":
            response = base_llm_http_handler.embedding(
                model=model,
                input=input,
                custom_llm_provider=custom_llm_provider,
                api_base=api_base,
                api_key=api_key,
                logging_obj=logging,
                timeout=timeout,
                model_response=EmbeddingResponse(),
                optional_params=optional_params,
                client=client,
                aembedding=aembedding,
                litellm_params={},
            )
        else:
            raise LiteLLMUnknownProvider(
                model=model, custom_llm_provider=custom_llm_provider
            )
        if (
            response is not None
            and hasattr(response, "_hidden_params")
            and isinstance(response, EmbeddingResponse)
        ):
            response._hidden_params["custom_llm_provider"] = custom_llm_provider

        if response is None:
            raise LiteLLMUnknownProvider(
                model=model, custom_llm_provider=custom_llm_provider
            )
        return response
    except Exception as e:
        ## LOGGING
        litellm_logging_obj.post_call(
            input=input,
            api_key=api_key,
            original_response=str(e),
        )
        ## Map to OpenAI Exception
        raise exception_type(
            model=model,
            original_exception=e,
            custom_llm_provider=custom_llm_provider,
            extra_kwargs=kwargs,
        )


def embedding(
    weight: Tensor,
    indices: Tensor,
    padding_idx: int = -1,
    scale_grad_by_freq: bool = False,
    sparse: bool = False,
) -> Tensor:
    if weight.dim() != 2:
        raise AssertionError(f"'weight' must be 2-D, got {weight.dim()}-D")
    weight_shape = weight.shape
    indices_shape = indices.shape

    if indices.ndim == 0:
        out_shape: tuple[int, ...] = (weight_shape[1],)
    elif indices.ndim == 1:
        out_shape = (indices_shape[0], weight_shape[1])
    else:
        out_shape = (*indices_shape, weight_shape[1])

    out_dtype = weight.dtype
    return weight.new_empty(out_shape, dtype=out_dtype)


def embedding(
    weight: list[int],
    indices: list[int],
    padding_idx: int = -1,
    scale_grad_by_freq: bool = False,
    sparse: bool = False,
):
    if len(weight) != 2:
        raise AssertionError(f"Expected weight to be 2D, but got {len(weight)}D")
    if len(indices) == 1:
        return index_select(weight, 0, indices)
    size = _copy(indices)
    size.append(weight[1])
    return size


def embedding(
    input: Tensor,
    weight: Tensor,
    padding_idx: int | None = None,
    max_norm: float | None = None,
    norm_type: float = 2.0,
    scale_grad_by_freq: bool = False,
    sparse: bool = False,
) -> Tensor:
    r"""Generate a simple lookup table that looks up embeddings in a fixed dictionary and size.

    This module is often used to retrieve word embeddings using indices.
    The input to the module is a list of indices, and the embedding matrix,
    and the output is the corresponding word embeddings.

    See :class:`torch.nn.Embedding` for more details.

    .. note::
        Note that the analytical gradients of this function with respect to
        entries in :attr:`weight` at the row specified by :attr:`padding_idx`
        are expected to differ from the numerical ones.

    .. note::
        Note that `:class:`torch.nn.Embedding` differs from this function in
        that it initializes the row of :attr:`weight` specified by
        :attr:`padding_idx` to all zeros on construction.

    Args:
        input (LongTensor): Tensor containing indices into the embedding matrix
        weight (Tensor): The embedding matrix (must be 2-D) with number of rows equal to the maximum possible index + 1,
            and number of columns equal to the embedding size
        padding_idx (int, optional): If specified, the entries at :attr:`padding_idx` do not contribute to the gradient;
                                     therefore, the embedding vector at :attr:`padding_idx` is not updated during training,
                                     i.e. it remains as a fixed "pad".
        max_norm (float, optional): If given, each embedding vector with norm larger than :attr:`max_norm`
                                    is renormalized to have norm :attr:`max_norm`.
                                    Note: this will modify :attr:`weight` in-place.
        norm_type (float, optional): The p of the p-norm to compute for the :attr:`max_norm` option. Default ``2``.
        scale_grad_by_freq (bool, optional): If given, this will scale gradients by the inverse of frequency of
                                                the words in the mini-batch. Default ``False``.
        sparse (bool, optional): If ``True``, gradient w.r.t. :attr:`weight` will be a sparse tensor. See Notes under
                                 :class:`torch.nn.Embedding` for more details regarding sparse gradients.

    Shape:
        - Input: LongTensor of arbitrary shape containing the indices to extract
        - Weight: Embedding matrix of floating point type with shape `(V, embedding_dim)`,
          where V = maximum index + 1 and embedding_dim = the embedding size
        - Output: `(*, embedding_dim)`, where `*` is the input shape

    Examples::

        >>> # a batch of 2 samples of 4 indices each
        >>> input = torch.tensor([[1, 2, 4, 5], [4, 3, 2, 9]])
        >>> # an embedding matrix containing 10 tensors of size 3
        >>> embedding_matrix = torch.rand(10, 3)
        >>> # xdoctest: +IGNORE_WANT("non-deterministic")
        >>> F.embedding(input, embedding_matrix)
        tensor([[[ 0.8490,  0.9625,  0.6753],
                 [ 0.9666,  0.7761,  0.6108],
                 [ 0.6246,  0.9751,  0.3618],
                 [ 0.4161,  0.2419,  0.7383]],

                [[ 0.6246,  0.9751,  0.3618],
                 [ 0.0237,  0.7794,  0.0528],
                 [ 0.9666,  0.7761,  0.6108],
                 [ 0.3385,  0.8612,  0.1867]]])

        >>> # example with padding_idx
        >>> weights = torch.rand(10, 3)
        >>> weights[0, :].zero_()
        >>> embedding_matrix = weights
        >>> input = torch.tensor([[0, 2, 0, 5]])
        >>> F.embedding(input, embedding_matrix, padding_idx=0)
        tensor([[[ 0.0000,  0.0000,  0.0000],
                 [ 0.5609,  0.5384,  0.8720],
                 [ 0.0000,  0.0000,  0.0000],
                 [ 0.6262,  0.2438,  0.7471]]])
    """
    if has_torch_function_variadic(input, weight):
        return handle_torch_function(
            embedding,
            (input, weight),
            input,
            weight,
            padding_idx=padding_idx,
            max_norm=max_norm,
            norm_type=norm_type,
            scale_grad_by_freq=scale_grad_by_freq,
            sparse=sparse,
        )
    if padding_idx is not None:
        if padding_idx > 0:
            if padding_idx >= weight.size(0):
                raise AssertionError("Padding_idx must be within num_embeddings")
        elif padding_idx < 0:
            if padding_idx < -weight.size(0):
                raise AssertionError("Padding_idx must be within num_embeddings")
            padding_idx = weight.size(0) + padding_idx
    else:
        padding_idx = -1
    if max_norm is not None:
        # Note [embedding_renorm contiguous]
        # `embedding_renorm_` will call .contiguous() on input anyways, so we
        # call it here and take advantage of the improved locality in the
        # `embedding` call below too.
        input = input.contiguous()
        # Note [embedding_renorm set_grad_enabled]
        # XXX: equivalent to
        # with torch.no_grad():
        #   torch.embedding_renorm_
        # remove once script supports set_grad_enabled
        _no_grad_embedding_renorm_(weight, input, max_norm, norm_type)
    return torch.embedding(weight, input, padding_idx, scale_grad_by_freq, sparse)


def embedding(
    weight: Tensor,
    indices: Tensor,
    padding_idx: int = -1,
    scale_grad_by_freq: bool = False,
    sparse: bool = False,
) -> Tensor:
    if weight.dim() != 2:
        raise AssertionError(f"'weight' must be 2-D, got {weight.dim()}-D")
    # Nb. scale_grad_by_freq is not used in the forward
    if indices.ndim <= 1:
        # We need this one as weight[indices] calls item() in these cases
        out = weight.index_select(0, indices)
        if indices.ndim == 0:
            out = out.squeeze(0)
        return out
    else:
        return weight[indices]


def embedding(weight, indices, padding_idx=-1, scale_grad_by_freq=False, sparse=False):
    if sparse:
        return fallback_handler(aten.embedding.default)(
            weight, indices, padding_idx, scale_grad_by_freq, sparse
        )

    assert not sparse
    assert isinstance(weight, TensorBox)
    assert isinstance(indices, TensorBox)
    assert "int" in str(indices.get_dtype())

    weight_loader = weight.make_loader()
    indices_loader = indices.make_loader()
    indices_ndim = len(indices.get_size())
    weight_size = weight.get_size()
    new_size = [*indices.get_size(), *weight_size[1:]]

    def fn(idx):
        assert len(idx) == len(new_size), f"{idx} != {new_size}"
        var_index = indices_loader(idx[:indices_ndim])
        weight_idx = [ops.indirect_indexing(var_index, weight_size[0])] + [
            *idx[indices_ndim:]
        ]
        return weight_loader(weight_idx)

    return Pointwise.create(
        device=weight.get_device(),
        dtype=weight.get_dtype(),
        inner_fn=fn,
        ranges=new_size,
    )


def embedding(
    g: jit_utils.GraphContext,
    weight,
    indices,
    padding_idx,
    scale_grad_by_freq,
    sparse,
):
    if scale_grad_by_freq and GLOBALS.export_training:
        raise errors.SymbolicValueError(
            "Unsupported: ONNX export of embedding with scale_grad_by_freq=True "
            "for training mode. ONNX does not support scaling the gradients.",
            weight,
        )
    if padding_idx >= 0 and GLOBALS.export_training:
        warnings.warn(
            "Warning: ONNX export of embedding with padding_idx >= 0 "
            "for training mode. "
            "ONNX does not support not updating the embedding vector at padding_idx during training.",
            stacklevel=2,
        )

    return g.op("Gather", weight, indices)


def embedding():
    # logic for parsing in - calling - parsing out model embedding calls
    pass


def embedding():
    # logic for parsing in - calling - parsing out model embedding calls
    pass


def embedding():
    # logic for parsing in - calling - parsing out model embedding calls
    pass


def embedding():
    # logic for parsing in - calling - parsing out model embedding calls
    pass


def embedding(
    model: str,
    input: list,
    model_response: EmbeddingResponse,
    api_key: Optional[str],
    api_base: Optional[str],
    logging_obj: Any,
    optional_params: dict,
    encoding=None,
):
    # Create completion URL
    if "https" in model:
        embeddings_url = model
    elif api_base:
        embeddings_url = f"{api_base}/v1/embeddings"
    else:
        raise OobaboogaError(
            status_code=404,
            message="API Base not set. Set one via completion(..,api_base='your-api-url')",
        )

    # Prepare request data
    data = {"input": input}
    if optional_params:
        data.update(optional_params)

    # Logging before API call
    if logging_obj:
        logging_obj.pre_call(
            input=input, api_key=api_key, additional_args={"complete_input_dict": data}
        )

    # Send POST request
    headers = oobabooga_config.validate_environment(
        api_key=api_key,
        headers={},
        model=model,
        messages=[],
        optional_params=optional_params,
        litellm_params={},
    )
    response = litellm.module_level_client.post(
        embeddings_url, headers=headers, json=data
    )
    completion_response = response.json()

    # Check for errors in response
    if "error" in completion_response:
        raise OobaboogaError(
            message=completion_response["error"],
            status_code=completion_response.get("status_code", 500),
        )

    # Process response data
    model_response.data = [
        {
            "embedding": completion_response["data"][0]["embedding"],
            "index": 0,
            "object": "embedding",
        }
    ]

    num_tokens = len(completion_response["data"][0]["embedding"])
    # Adding metadata to response
    setattr(
        model_response,
        "usage",
        Usage(prompt_tokens=num_tokens, total_tokens=num_tokens),
    )
    model_response.object = "list"
    model_response.model = model

    return model_response


def embedding():
    # logic for parsing in - calling - parsing out model embedding calls
    pass


def embedding(
    model: str,
    input: list,
    model_response: EmbeddingResponse,
    logging_obj: LiteLLMLoggingObj,
    optional_params: dict,
    headers: dict,
    encoding: Any,
    data: Optional[Union[dict, CohereEmbeddingRequest]] = None,
    complete_api_base: Optional[str] = None,
    api_key: Optional[str] = None,
    aembedding: Optional[bool] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = httpx.Timeout(None),
    client: Optional[Union[HTTPHandler, AsyncHTTPHandler]] = None,
):
    headers = validate_environment(api_key, headers=headers)
    embed_url = complete_api_base or "https://api.cohere.ai/v1/embed"
    model = model

    data = data or CohereEmbeddingConfig()._transform_request(
        model=model, input=input, inference_params=optional_params
    )

    ## ROUTING
    if aembedding is True:
        return async_embedding(
            model=model,
            data=data,
            input=input,
            model_response=model_response,
            timeout=timeout,
            logging_obj=logging_obj,
            optional_params=optional_params,
            api_base=embed_url,
            api_key=api_key,
            headers=headers,
            encoding=encoding,
            client=(
                client
                if client is not None and isinstance(client, AsyncHTTPHandler)
                else None
            ),
        )

    ## LOGGING
    logging_obj.pre_call(
        input=input,
        api_key=api_key,
        additional_args={"complete_input_dict": data},
    )

    ## COMPLETION CALL
    if client is None or not isinstance(client, HTTPHandler):
        client = HTTPHandler(concurrent_limit=1)

    response = client.post(embed_url, headers=headers, data=json.dumps(data))

    return CohereEmbeddingConfig()._transform_response(
        response=response,
        api_key=api_key,
        logging_obj=logging_obj,
        data=data,
        model_response=model_response,
        model=model,
        encoding=encoding,
        input=input,
    )


def embedding(
  scope: Scope, num_embeddings: int, features: int, init_fn=default_embed_init
) -> Embedding:
  """Creates embedding dataclass.

  Args:
    num_embeddings: number of embeddings.
    features: Number of feature dimensions for each embedding.
    embedding_init: embedding initializer.

  Returns:
    Embedding dataclass with lookup and attend methods.
  """
  table = scope.param('table', init_fn, (num_embeddings, features))
  return Embedding(table)  # type: ignore

