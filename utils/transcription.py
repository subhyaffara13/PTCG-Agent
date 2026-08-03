from typing import Any, List, Optional, Union

def transcription(
    model: str,
    file: FileTypes,
    ## OPTIONAL OPENAI PARAMS ##
    language: Optional[str] = None,
    prompt: Optional[str] = None,
    response_format: Optional[
        Literal["json", "text", "srt", "verbose_json", "vtt"]
    ] = None,
    timestamp_granularities: Optional[List[Literal["word", "segment"]]] = None,
    temperature: Optional[int] = None,  # openai defaults this to 0
    ## LITELLM PARAMS ##
    user: Optional[str] = None,
    timeout=600,  # default to 10 minutes
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    api_version: Optional[str] = None,
    max_retries: Optional[int] = None,
    custom_llm_provider=None,
    **kwargs,
) -> Union[TranscriptionResponse, Coroutine[Any, Any, TranscriptionResponse]]:
    """
    Calls openai + azure whisper endpoints.

    Allows router to load balance between them
    """
    litellm_call_id = kwargs.get("litellm_call_id", None)
    proxy_server_request = kwargs.get("proxy_server_request", None)
    model_info = kwargs.get("model_info", None)
    metadata = kwargs.get("metadata", None)
    atranscription = kwargs.pop("atranscription", False)
    litellm_logging_obj: LiteLLMLoggingObj = kwargs.get("litellm_logging_obj")  # type: ignore
    extra_headers = kwargs.get("extra_headers", None)
    shared_session = kwargs.get("shared_session", None)
    kwargs.pop("tags", [])
    non_default_params = get_non_default_transcription_params(kwargs)

    client: Optional[
        Union[
            openai.AsyncOpenAI,
            openai.OpenAI,
            openai.AzureOpenAI,
            openai.AsyncAzureOpenAI,
        ]
    ] = kwargs.pop("client", None)

    if litellm_logging_obj:
        litellm_logging_obj.model_call_details["client"] = str(client)

    if max_retries is None:
        max_retries = openai.DEFAULT_MAX_RETRIES

    model_response = litellm.utils.TranscriptionResponse()

    model, custom_llm_provider, dynamic_api_key, api_base = get_llm_provider(
        model=model,
        custom_llm_provider=custom_llm_provider,
        api_base=api_base,
        api_key=api_key,
    )  # type: ignore

    api_key = dynamic_api_key if dynamic_api_key is not None else api_key

    optional_params = get_optional_params_transcription(
        model=model,
        language=language,
        prompt=prompt,
        response_format=response_format,
        timestamp_granularities=timestamp_granularities,
        temperature=temperature,
        custom_llm_provider=custom_llm_provider,
        **non_default_params,
    )

    litellm_params_dict = get_litellm_params(**kwargs)

    litellm_logging_obj.update_environment_variables(
        model=model,
        user=user,
        optional_params={},
        litellm_params={
            "litellm_call_id": litellm_call_id,
            "proxy_server_request": proxy_server_request,
            "model_info": model_info,
            "metadata": metadata,
            "preset_cache_key": None,
            "stream_response": {},
            **kwargs,
        },
        custom_llm_provider=custom_llm_provider,
    )

    response: Optional[
        Union[TranscriptionResponse, Coroutine[Any, Any, TranscriptionResponse]]
    ] = None

    provider_config = ProviderConfigManager.get_provider_audio_transcription_config(
        model=model,
        provider=LlmProviders(custom_llm_provider),
    )

    if custom_llm_provider == "azure" and provider_config is None:
        # azure configs
        api_base = api_base or litellm.api_base or get_secret_str("AZURE_API_BASE")

        api_version = (
            api_version or litellm.api_version or get_secret_str("AZURE_API_VERSION")
        )

        azure_ad_token = kwargs.pop("azure_ad_token", None) or get_secret_str(
            "AZURE_AD_TOKEN"
        )

        api_key = (
            api_key
            or litellm.api_key
            or litellm.azure_key
            or get_secret_str("AZURE_API_KEY")
        )

        optional_params["extra_headers"] = extra_headers

        response = azure_audio_transcriptions.audio_transcriptions(
            model=model,
            audio_file=file,
            optional_params=optional_params,
            model_response=model_response,
            atranscription=atranscription,
            client=client,
            timeout=timeout,
            logging_obj=litellm_logging_obj,
            api_base=api_base,
            api_key=api_key,
            api_version=api_version,
            azure_ad_token=azure_ad_token,
            max_retries=max_retries,
            litellm_params=litellm_params_dict,
        )
    elif custom_llm_provider == "openai" or (
        custom_llm_provider in litellm.openai_compatible_providers
    ):
        api_base = (
            api_base
            or litellm.api_base
            or get_secret("OPENAI_BASE_URL")
            or get_secret("OPENAI_API_BASE")
            or "https://api.openai.com/v1"
        )  # type: ignore
        openai.organization = (
            litellm.organization
            or get_secret("OPENAI_ORGANIZATION")
            or None  # default - https://github.com/openai/openai-python/blob/284c1799070c723c6a553337134148a7ab088dd8/openai/util.py#L105
        )
        # set API KEY

        api_key = api_key or litellm.api_key or litellm.openai_key or get_secret("OPENAI_API_KEY")  # type: ignore
        response = openai_audio_transcriptions.audio_transcriptions(
            model=model,
            audio_file=file,
            optional_params=optional_params,
            model_response=model_response,
            atranscription=atranscription,
            client=client,
            timeout=timeout,
            logging_obj=litellm_logging_obj,
            max_retries=max_retries,
            api_base=api_base,
            api_key=api_key,
            provider_config=provider_config,
            litellm_params=litellm_params_dict,
            shared_session=shared_session,
        )
    elif custom_llm_provider == "nvidia_riva":
        # NVIDIA Riva is gRPC-based, not HTTP. It has its own dedicated handler
        # rather than going through base_llm_http_handler.
        response = nvidia_riva_audio_transcriptions.audio_transcriptions(
            model=model,
            audio_file=file,
            optional_params=optional_params,
            litellm_params=litellm_params_dict,
            model_response=model_response,
            atranscription=atranscription,
            timeout=timeout,
            logging_obj=litellm_logging_obj,
            api_base=api_base,
            api_key=api_key,
            provider_config=(
                provider_config
                if isinstance(provider_config, NvidiaRivaAudioTranscriptionConfig)
                else None
            ),
        )
    elif custom_llm_provider == "soniox":
        from litellm.llms.soniox.audio_transcription.handler import (
            SonioxAudioTranscriptionHandler,
        )

        response = SonioxAudioTranscriptionHandler().audio_transcriptions(
            model=model,
            audio_file=file,
            optional_params=optional_params,
            litellm_params=litellm_params_dict,
            model_response=model_response,
            atranscription=atranscription,
            client=(
                client
                if client is not None
                and (
                    isinstance(client, HTTPHandler)
                    or isinstance(client, AsyncHTTPHandler)
                )
                else None
            ),
            timeout=timeout,
            max_retries=max_retries,
            logging_obj=litellm_logging_obj,
            api_base=api_base,
            api_key=api_key,
            headers=extra_headers,
            provider_config=provider_config,  # type: ignore[arg-type]
        )
    elif provider_config is not None:
        response = base_llm_http_handler.audio_transcriptions(
            model=model,
            audio_file=file,
            optional_params=optional_params,
            litellm_params=litellm_params_dict,
            model_response=model_response,
            atranscription=atranscription,
            client=(
                client
                if client is not None
                and (
                    isinstance(client, HTTPHandler)
                    or isinstance(client, AsyncHTTPHandler)
                )
                else None
            ),
            timeout=timeout,
            max_retries=max_retries,
            logging_obj=litellm_logging_obj,
            api_base=api_base,
            api_key=api_key,
            custom_llm_provider=custom_llm_provider,
            headers={},
            provider_config=provider_config,
            shared_session=shared_session,
        )

    # Store duration in _hidden_params for cost calculation without
    # exposing it in the response body (see sync path comment above).
    if response is not None and not isinstance(response, Coroutine):
        existing_duration = getattr(response, "duration", None)
        if existing_duration is None:
            calculated_duration = calculate_request_duration(file)
            if calculated_duration is not None:
                response._hidden_params["audio_transcription_duration"] = (
                    calculated_duration
                )

    if response is None:
        raise ValueError("Unmapped provider passed in. Unable to get the response.")
    return response

