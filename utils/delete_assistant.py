
def delete_assistant(
    custom_llm_provider: Literal["openai", "azure"],
    assistant_id: str,
    client: Optional[Any] = None,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    api_version: Optional[str] = None,
    **kwargs,
) -> Union[AssistantDeleted, Coroutine[Any, Any, AssistantDeleted]]:
    optional_params = GenericLiteLLMParams(
        api_key=api_key, api_base=api_base, api_version=api_version, **kwargs
    )

    litellm_params_dict = get_litellm_params(**kwargs)

    async_delete_assistants: Optional[bool] = kwargs.pop(
        "async_delete_assistants", None
    )
    if async_delete_assistants is not None and not isinstance(
        async_delete_assistants, bool
    ):
        raise ValueError(
            "Invalid value passed in for async_delete_assistants. Only bool or None allowed"
        )

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

    response: Optional[
        Union[AssistantDeleted, Coroutine[Any, Any, AssistantDeleted]]
    ] = None
    if custom_llm_provider == "openai":
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
            or None
        )
        # set API KEY
        api_key = (
            optional_params.api_key
            or litellm.api_key
            or litellm.openai_key
            or os.getenv("OPENAI_API_KEY")
        )

        response = openai_assistants_api.delete_assistant(
            api_base=api_base,
            api_key=api_key,
            timeout=timeout,
            max_retries=optional_params.max_retries,
            organization=organization,
            assistant_id=assistant_id,
            client=client,
            async_delete_assistants=async_delete_assistants,
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
        azure_ad_token: Optional[str] = None
        if extra_body is not None:
            azure_ad_token = extra_body.pop("azure_ad_token", None)
        else:
            azure_ad_token = get_secret("AZURE_AD_TOKEN")  # type: ignore

        if isinstance(client, OpenAI):
            client = None  # only pass client if it's AzureOpenAI

        response = azure_assistants_api.delete_assistant(
            assistant_id=assistant_id,
            api_base=api_base,
            api_key=api_key,
            azure_ad_token=azure_ad_token,
            api_version=api_version,
            timeout=timeout,
            max_retries=optional_params.max_retries,
            client=client,
            async_delete_assistants=async_delete_assistants,
            litellm_params=litellm_params_dict,
        )
    else:
        raise litellm.exceptions.BadRequestError(
            message="LiteLLM doesn't support {} for 'delete_assistant'. Only 'openai' is supported.".format(
                custom_llm_provider
            ),
            model="n/a",
            llm_provider=custom_llm_provider,
            response=httpx.Response(
                status_code=400,
                content="Unsupported provider",
                request=httpx.Request(
                    method="delete_assistant", url="https://github.com/BerriAI/litellm"
                ),
            ),
        )
    if response is None:
        raise litellm.exceptions.InternalServerError(
            message="No response returned from 'delete_assistant'",
            model="n/a",
            llm_provider=custom_llm_provider,
        )
    return response

