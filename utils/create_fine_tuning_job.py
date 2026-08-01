
def create_fine_tuning_job(
    model: str,
    training_file: str,
    hyperparameters: Optional[dict] = {},
    suffix: Optional[str] = None,
    validation_file: Optional[str] = None,
    integrations: Optional[List[str]] = None,
    seed: Optional[int] = None,
    custom_llm_provider: Literal["openai", "azure", "vertex_ai"] = "openai",
    extra_headers: Optional[Dict[str, str]] = None,
    extra_body: Optional[Dict[str, str]] = None,
    **kwargs,
) -> Union[LiteLLMFineTuningJob, Coroutine[Any, Any, LiteLLMFineTuningJob]]:
    """
    Creates a fine-tuning job which begins the process of creating a new model from a given dataset.

    Response includes details of the enqueued job including job status and the name of the fine-tuned models once complete

    """
    try:
        _is_async = kwargs.pop("acreate_fine_tuning_job", False) is True
        optional_params = GenericLiteLLMParams(**kwargs)

        # handle hyperparameters
        hyperparameters = hyperparameters or {}  # original hyperparameters

        # For Azure, extract Azure-specific hyperparameters before creating OpenAI-spec hyperparameters
        azure_specific_hyperparams = {}
        if custom_llm_provider == "azure":
            azure_hyperparameter_keys = ["prompt_loss_weight"]
            for key in azure_hyperparameter_keys:
                if key in hyperparameters:
                    azure_specific_hyperparams[key] = hyperparameters.pop(key)

        _oai_hyperparameters: Hyperparameters = Hyperparameters(
            **hyperparameters
        )  # Typed Hyperparameters for OpenAI Spec
        timeout = _resolve_fine_tuning_timeout(
            optional_params.timeout or kwargs.get("request_timeout", 600),
            custom_llm_provider,
        )

        # OpenAI
        if custom_llm_provider == "openai":
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

            create_fine_tuning_job_data_dict = _build_fine_tuning_job_data(
                model,
                training_file,
                _oai_hyperparameters,
                suffix,
                validation_file,
                integrations,
                seed,
            ).model_dump(exclude_none=True)

            response = openai_fine_tuning_apis_instance.create_fine_tuning_job(
                api_base=api_base,
                api_key=api_key,
                api_version=optional_params.api_version,
                organization=organization,
                create_fine_tuning_job_data=create_fine_tuning_job_data_dict,
                timeout=timeout,
                max_retries=optional_params.max_retries,
                _is_async=_is_async,
                client=kwargs.get(
                    "client", None
                ),  # note, when we add this to `GenericLiteLLMParams` it impacts a lot of other tests + linting
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

            # Prepare Azure-specific parameters for extra_body
            extra_body = _prepare_azure_extra_body(
                extra_body, kwargs, azure_specific_hyperparams
            )

            create_fine_tuning_job_data_dict = _build_fine_tuning_job_data(
                model,
                training_file,
                _oai_hyperparameters,
                suffix,
                validation_file,
                integrations,
                seed,
            ).model_dump(exclude_none=True)

            # Add extra_body if it has Azure-specific parameters
            if extra_body:
                create_fine_tuning_job_data_dict["extra_body"] = extra_body

            response = azure_fine_tuning_apis_instance.create_fine_tuning_job(
                api_base=api_base,
                api_key=api_key,
                api_version=api_version,
                create_fine_tuning_job_data=create_fine_tuning_job_data_dict,
                timeout=timeout,
                max_retries=optional_params.max_retries,
                _is_async=_is_async,
                organization=optional_params.organization,
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
            response = vertex_fine_tuning_apis_instance.create_fine_tuning_job(
                _is_async=_is_async,
                create_fine_tuning_job_data=_build_fine_tuning_job_data(
                    model,
                    training_file,
                    _oai_hyperparameters,
                    suffix,
                    validation_file,
                    integrations,
                    seed,
                ),
                vertex_credentials=vertex_credentials,
                vertex_project=vertex_ai_project,
                vertex_location=vertex_ai_location,
                timeout=timeout,
                api_base=api_base,
                kwargs=kwargs,
                original_hyperparameters=hyperparameters,
            )
        else:
            raise litellm.exceptions.BadRequestError(
                message="LiteLLM doesn't support {} for 'create_batch'. Only 'openai' is supported.".format(
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
        verbose_logger.error("got exception in create_fine_tuning_job=%s", str(e))
        raise e

