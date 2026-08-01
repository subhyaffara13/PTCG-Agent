
def run_thread(
    custom_llm_provider: Literal["openai", "azure"],
    thread_id: str,
    assistant_id: str,
    additional_instructions: Optional[str] = None,
    instructions: Optional[str] = None,
    metadata: Optional[dict] = None,
    model: Optional[str] = None,
    stream: Optional[bool] = None,
    tools: Optional[Iterable[AssistantToolParam]] = None,
    client: Optional[Any] = None,
    event_handler: Optional[AssistantEventHandler] = None,  # for stream=True calls
    **kwargs,
) -> Run:
    """Run a given thread + assistant."""
    arun_thread = kwargs.pop("arun_thread", None)
    optional_params = GenericLiteLLMParams(**kwargs)
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

    response: Optional[Run] = None
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

        response = openai_assistants_api.run_thread(
            thread_id=thread_id,
            assistant_id=assistant_id,
            additional_instructions=additional_instructions,
            instructions=instructions,
            metadata=metadata,
            model=model,
            stream=stream,
            tools=tools,
            api_base=api_base,
            api_key=api_key,
            timeout=timeout,
            max_retries=optional_params.max_retries,
            organization=organization,
            client=client,
            arun_thread=arun_thread,
            event_handler=event_handler,
        )
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
        azure_ad_token = None
        if extra_body is not None:
            azure_ad_token = extra_body.pop("azure_ad_token", None)
        else:
            azure_ad_token = get_secret("AZURE_AD_TOKEN")  # type: ignore

        response = azure_assistants_api.run_thread(
            thread_id=thread_id,
            assistant_id=assistant_id,
            additional_instructions=additional_instructions,
            instructions=instructions,
            metadata=metadata,
            model=model,
            stream=stream,
            tools=tools,
            api_base=str(api_base) if api_base is not None else None,
            api_key=str(api_key) if api_key is not None else None,
            api_version=str(api_version) if api_version is not None else None,
            azure_ad_token=str(azure_ad_token) if azure_ad_token is not None else None,
            timeout=timeout,
            max_retries=optional_params.max_retries,
            client=client,
            arun_thread=arun_thread,
            litellm_params=litellm_params_dict,
        )  # type: ignore
    else:
        raise litellm.exceptions.BadRequestError(
            message="LiteLLM doesn't support {} for 'run_thread'. Only 'openai' is supported.".format(
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
    return response  # type: ignore

