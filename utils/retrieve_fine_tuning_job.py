
def retrieve_fine_tuning_job(
    fine_tuning_job_id: str,
    custom_llm_provider: Literal["openai", "azure", "vertex_ai"] = "openai",
    extra_headers: Optional[Dict[str, str]] = None,
    extra_body: Optional[Dict[str, str]] = None,
    **kwargs,
) -> Union[LiteLLMFineTuningJob, Coroutine[Any, Any, LiteLLMFineTuningJob]]:
    """
    Get info about a fine-tuning job.
    """
    try:
        optional_params = GenericLiteLLMParams(**kwargs)
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

        _is_async = kwargs.pop("aretrieve_fine_tuning_job", False) is True

        # OpenAI
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
            api_key = (
                optional_params.api_key
                or litellm.api_key
                or litellm.openai_key
                or os.getenv("OPENAI_API_KEY")
            )

            response = openai_fine_tuning_apis_instance.retrieve_fine_tuning_job(
                api_base=api_base,
                api_key=api_key,
                api_version=optional_params.api_version,
                organization=organization,
                fine_tuning_job_id=fine_tuning_job_id,
                timeout=timeout,
                max_retries=optional_params.max_retries,
                _is_async=_is_async,
                client=kwargs.get("client", None),
            )
        # Azure OpenAI
        elif custom_llm_provider == "azure":
            api_base = optional_params.api_base or litellm.api_base or get_secret_str("AZURE_API_BASE")  # type: ignore

            api_version = (
                optional_params.api_version
                or litellm.api_version
                or get_secret_str("AZURE_API_VERSION")
            )  # type: ignore

            api_key = (
                optional_params.api_key
                or litellm.api_key
                or litellm.azure_key
                or get_secret_str("AZURE_OPENAI_API_KEY")
                or get_secret_str("AZURE_API_KEY")
            )  # type: ignore

            extra_body = optional_params.get("extra_body", {})
            if extra_body is not None:
                extra_body.pop("azure_ad_token", None)
            else:
                get_secret_str("AZURE_AD_TOKEN")  # type: ignore

            response = azure_fine_tuning_apis_instance.retrieve_fine_tuning_job(
                api_base=api_base,
                api_key=api_key,
                api_version=api_version,
                fine_tuning_job_id=fine_tuning_job_id,
                timeout=timeout,
                max_retries=optional_params.max_retries,
                _is_async=_is_async,
                organization=optional_params.organization,
            )
        else:
            raise litellm.exceptions.BadRequestError(
                message="LiteLLM doesn't support {} for 'retrieve_fine_tuning_job'. Only 'openai' and 'azure' are supported.".format(
                    custom_llm_provider
                ),
                model="n/a",
                llm_provider=custom_llm_provider,
                response=httpx.Response(
                    status_code=400,
                    content="Unsupported provider",
                    request=httpx.Request(method="retrieve_fine_tuning_job", url="https://github.com/BerriAI/litellm"),  # type: ignore
                ),
            )
        return response
    except Exception as e:
        raise e

