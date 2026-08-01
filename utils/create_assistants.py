
def create_assistants(
    custom_llm_provider: Literal["openai", "azure"],
    model: str,
    name: Optional[str] = None,
    description: Optional[str] = None,
    instructions: Optional[str] = None,
    tools: Optional[List[Dict[str, Any]]] = None,
    tool_resources: Optional[Dict[str, Any]] = None,
    metadata: Optional[Dict[str, str]] = None,
    temperature: Optional[float] = None,
    top_p: Optional[float] = None,
    response_format: Optional[Union[str, Dict[str, str]]] = None,
    client: Optional[Any] = None,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    api_version: Optional[str] = None,
    **kwargs,
) -> Union[Assistant, Coroutine[Any, Any, Assistant]]:
    async_create_assistants: Optional[bool] = kwargs.pop(
        "async_create_assistants", None
    )
    if async_create_assistants is not None and not isinstance(
        async_create_assistants, bool
    ):
        raise ValueError(
            "Invalid value passed in for async_create_assistants. Only bool or None allowed"
        )
    optional_params = GenericLiteLLMParams(
        api_key=api_key, api_base=api_base, api_version=api_version, **kwargs
    )
    litellm_params_dict = get_litellm_params(**kwargs)

    ### TIMEOUT LOGIC ###
    timeout = optional_params.timeout or kwargs.get("request_timeout", 600) or 600
    # set timeout for 10 minutes by default

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

    create_assistant_data = {
        "model": model,
        "name": name,
        "description": description,
        "instructions": instructions,
        "tools": tools,
        "tool_resources": tool_resources,
        "metadata": metadata,
        "temperature": temperature,
        "top_p": top_p,
        "response_format": response_format,
    }

    # only send params that are not None
    create_assistant_data = {
        k: v for k, v in create_assistant_data.items() if v is not None
    }

    response: Optional[Union[Coroutine[Any, Any, Assistant], Assistant]] = None
    if custom_llm_provider == "openai":
        api_base = (
            optional_params.api_base  # for deepinfra/perplexity/anyscale/groq we check in get_llm_provider and pass in the api base from there
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

        response = openai_assistants_api.create_assistants(
            api_base=api_base,
            api_key=api_key,
            timeout=timeout,
            max_retries=optional_params.max_retries,
            organization=organization,
            create_assistant_data=create_assistant_data,
            client=client,
            async_create_assistants=async_create_assistants,  # type: ignore
        )  # type: ignore
    elif custom_llm_provider == "azure":
        api_base = (
            optional_params.api_base or litellm.api_base or get_secret("AZURE_API_BASE")
        )  # type: ignore

        api_version = (
            optional_params.api_version
            or litellm.api_version
            or get_secret("AZURE_API_VERSION")
        )  # type: ignore

        api_key = (
            optional_params.api_key
            or litellm.api_key
            or litellm.azure_key
            or get_secret("AZURE_OPENAI_API_KEY")
            or get_secret("AZURE_API_KEY")
        )  # type: ignore

        extra_body = optional_params.get("extra_body", {})
        azure_ad_token: Optional[str] = None
        if extra_body is not None:
            azure_ad_token = extra_body.pop("azure_ad_token", None)
        else:
            azure_ad_token = get_secret("AZURE_AD_TOKEN")  # type: ignore

        if isinstance(client, OpenAI):
            client = None  # only pass client if it's AzureOpenAI

        response = azure_assistants_api.create_assistants(
            api_base=api_base,
            api_key=api_key,
            azure_ad_token=azure_ad_token,
            api_version=api_version,
            timeout=timeout,
            max_retries=optional_params.max_retries,
            client=client,
            async_create_assistants=async_create_assistants,
            create_assistant_data=create_assistant_data,
            litellm_params=litellm_params_dict,
        )
    else:
        raise litellm.exceptions.BadRequestError(
            message="LiteLLM doesn't support {} for 'create_assistants'. Only 'openai' is supported.".format(
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
    if response is None:
        raise litellm.exceptions.InternalServerError(
            message="No response returned from 'create_assistants'",
            model=model,
            llm_provider=custom_llm_provider,
        )
    return response

