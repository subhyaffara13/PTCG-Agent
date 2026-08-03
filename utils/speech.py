from typing import Any, Optional, Union

def speech(
    model: str,
    input: str,
    voice: Optional[Union[str, dict]] = None,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    api_version: Optional[str] = None,
    organization: Optional[str] = None,
    project: Optional[str] = None,
    max_retries: Optional[int] = None,
    metadata: Optional[dict] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    response_format: Optional[str] = None,
    speed: Optional[int] = None,
    instructions: Optional[str] = None,
    client=None,
    headers: Optional[dict] = None,
    custom_llm_provider: Optional[str] = None,
    aspeech: Optional[bool] = None,
    **kwargs,
) -> Union[HttpxBinaryResponseContent, Coroutine[Any, Any, HttpxBinaryResponseContent]]:
    user = kwargs.get("user", None)
    litellm_call_id: Optional[str] = kwargs.get("litellm_call_id", None)
    proxy_server_request = kwargs.get("proxy_server_request", None)
    extra_headers = kwargs.get("extra_headers", None)
    model_info = kwargs.get("model_info", None)
    shared_session = kwargs.get("shared_session", None)
    model, custom_llm_provider, dynamic_api_key, api_base = get_llm_provider(
        model=model, custom_llm_provider=custom_llm_provider, api_base=api_base
    )  # type: ignore
    kwargs.pop("tags", [])

    optional_params = {}
    if response_format is not None:
        optional_params["response_format"] = response_format
    if speed is not None:
        optional_params["speed"] = speed  # type: ignore
    if instructions is not None:
        optional_params["instructions"] = instructions

    if timeout is None:
        timeout = litellm.request_timeout

    if max_retries is None:
        max_retries = litellm.num_retries or openai.DEFAULT_MAX_RETRIES
    litellm_params_dict = get_litellm_params(**kwargs)

    # Get provider-specific text-to-speech config and map parameters
    text_to_speech_provider_config = (
        ProviderConfigManager.get_provider_text_to_speech_config(
            model=model,
            provider=litellm.LlmProviders(custom_llm_provider),
        )
    )

    # Map OpenAI params to provider-specific params if config exists
    if text_to_speech_provider_config is not None:
        voice, optional_params = text_to_speech_provider_config.map_openai_params(
            model=model,
            optional_params=optional_params,
            voice=voice,
            drop_params=False,
            kwargs=kwargs,
        )

    logging_obj: LiteLLMLoggingObj = cast(
        LiteLLMLoggingObj, kwargs.get("litellm_logging_obj")
    )
    logging_obj.update_environment_variables(
        model=model,
        user=user,
        optional_params=optional_params,
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
    response: Union[
        HttpxBinaryResponseContent,
        Coroutine[Any, Any, HttpxBinaryResponseContent],
        None,
    ] = None
    if (
        custom_llm_provider == "openai"
        or custom_llm_provider in litellm.openai_compatible_providers
    ):
        if voice is None or not (isinstance(voice, str)):
            raise litellm.BadRequestError(
                message="'voice' is required to be passed as a string for OpenAI TTS",
                model=model,
                llm_provider=custom_llm_provider,
            )
        api_base = (
            api_base  # for deepinfra/perplexity/anyscale/groq/friendliai we check in get_llm_provider and pass in the api base from there
            or litellm.api_base
            or get_secret("OPENAI_BASE_URL")
            or get_secret("OPENAI_API_BASE")
            or "https://api.openai.com/v1"
        )  # type: ignore
        # set API KEY
        api_key = (
            api_key
            or litellm.api_key  # for deepinfra/perplexity/anyscale we check in get_llm_provider and pass in the api key from there
            or litellm.openai_key
            or get_secret("OPENAI_API_KEY")
        )  # type: ignore

        organization = (
            organization
            or litellm.organization
            or get_secret("OPENAI_ORGANIZATION")
            or None  # default - https://github.com/openai/openai-python/blob/284c1799070c723c6a553337134148a7ab088dd8/openai/util.py#L105
        )  # type: ignore

        project = (
            project
            or litellm.project
            or get_secret("OPENAI_PROJECT")
            or None  # default - https://github.com/openai/openai-python/blob/284c1799070c723c6a553337134148a7ab088dd8/openai/util.py#L105
        )  # type: ignore

        headers = headers or litellm.headers

        response = openai_chat_completions.audio_speech(
            model=model,
            input=input,
            voice=voice,
            optional_params=optional_params,
            api_key=api_key,
            api_base=api_base,
            organization=organization,
            project=project,
            max_retries=max_retries,
            timeout=timeout,
            client=client,  # pass AsyncOpenAI, OpenAI client
            aspeech=aspeech,
            shared_session=shared_session,
        )
    elif custom_llm_provider == "azure":
        # Check if this is Azure Speech Service (Cognitive Services TTS)
        if model.startswith("speech/"):
            from litellm.llms.azure.text_to_speech.transformation import (
                AzureAVATextToSpeechConfig,
            )

            # Azure AVA (Cognitive Services) Text-to-Speech
            if text_to_speech_provider_config is None:
                raise litellm.BadRequestError(
                    message="Azure Speech Service configuration not found",
                    model=model,
                    llm_provider=custom_llm_provider,
                )

            # Cast to specific Azure config type to access dispatch method
            azure_config = cast(
                AzureAVATextToSpeechConfig, text_to_speech_provider_config
            )

            response = azure_config.dispatch_text_to_speech(  # type: ignore
                model=model,
                input=input,
                voice=voice,
                optional_params=optional_params,
                litellm_params_dict=litellm_params_dict,
                logging_obj=logging_obj,
                timeout=timeout,
                extra_headers=extra_headers,
                base_llm_http_handler=base_llm_http_handler,
                aspeech=aspeech or False,
                api_base=api_base,
                api_key=api_key,
                **kwargs,
            )
        else:
            # Azure OpenAI TTS
            if voice is None or not (isinstance(voice, str)):
                raise litellm.BadRequestError(
                    message="'voice' is required to be passed as a string for Azure TTS",
                    model=model,
                    llm_provider=custom_llm_provider,
                )
            api_base = api_base or litellm.api_base or get_secret("AZURE_API_BASE")  # type: ignore

            api_version = api_version or litellm.api_version or get_secret("AZURE_API_VERSION")  # type: ignore

            api_key = (
                api_key
                or litellm.api_key
                or litellm.azure_key
                or get_secret("AZURE_OPENAI_API_KEY")
                or get_secret("AZURE_API_KEY")
            )  # type: ignore

            azure_ad_token: Optional[str] = optional_params.get("extra_body", {}).pop(  # type: ignore
                "azure_ad_token", None
            ) or get_secret(
                "AZURE_AD_TOKEN"
            )
            azure_ad_token_provider = kwargs.get("azure_ad_token_provider", None)

            if extra_headers:
                optional_params["extra_headers"] = extra_headers

            response = azure_chat_completions.audio_speech(
                model=model,
                input=input,
                voice=voice,
                optional_params=optional_params,
                api_key=api_key,
                api_base=api_base,
                api_version=api_version,
                azure_ad_token=azure_ad_token,
                azure_ad_token_provider=azure_ad_token_provider,
                organization=organization,
                max_retries=max_retries,
                timeout=timeout,
                client=client,  # pass AsyncOpenAI, OpenAI client
                aspeech=aspeech,
                litellm_params=litellm_params_dict,
            )
    elif custom_llm_provider == "elevenlabs":
        from litellm.llms.elevenlabs.text_to_speech.transformation import (
            ElevenLabsTextToSpeechConfig,
        )

        if text_to_speech_provider_config is None:
            text_to_speech_provider_config = ElevenLabsTextToSpeechConfig()

        elevenlabs_config = cast(
            ElevenLabsTextToSpeechConfig, text_to_speech_provider_config
        )

        voice_id = voice if isinstance(voice, str) else None
        if voice_id is None or not voice_id.strip():
            raise litellm.BadRequestError(
                message="'voice' must resolve to an ElevenLabs voice id for ElevenLabs TTS",
                model=model,
                llm_provider=custom_llm_provider,
            )
        voice_id = voice_id.strip()

        query_params = kwargs.pop(
            ElevenLabsTextToSpeechConfig.ELEVENLABS_QUERY_PARAMS_KEY, None
        )
        if isinstance(query_params, dict):
            litellm_params_dict[
                ElevenLabsTextToSpeechConfig.ELEVENLABS_QUERY_PARAMS_KEY
            ] = query_params

        litellm_params_dict[ElevenLabsTextToSpeechConfig.ELEVENLABS_VOICE_ID_KEY] = (
            voice_id
        )

        if api_base is not None:
            litellm_params_dict["api_base"] = api_base
        if api_key is not None:
            litellm_params_dict["api_key"] = api_key

        response = base_llm_http_handler.text_to_speech_handler(
            model=model,
            input=input,
            voice=voice_id,
            text_to_speech_provider_config=elevenlabs_config,
            text_to_speech_optional_params=optional_params,
            custom_llm_provider=custom_llm_provider,
            litellm_params=litellm_params_dict,
            logging_obj=logging_obj,
            timeout=timeout,
            extra_headers=extra_headers,
            client=client,
            _is_async=aspeech or False,
        )
    elif custom_llm_provider == "vertex_ai" or custom_llm_provider == "vertex_ai_beta":
        from litellm.llms.vertex_ai.text_to_speech.transformation import (
            VertexAITextToSpeechConfig,
        )

        generic_optional_params = GenericLiteLLMParams(**kwargs)

        # Handle Gemini models separately (they use speech_to_completion_bridge)
        if "gemini" in model:
            from .endpoints.speech.speech_to_completion_bridge.handler import (
                speech_to_completion_bridge_handler,
            )

            return speech_to_completion_bridge_handler.speech(
                model=model,
                input=input,
                voice=voice,
                optional_params=optional_params,
                litellm_params=litellm_params_dict,
                headers=headers or {},
                logging_obj=logging_obj,
                custom_llm_provider=custom_llm_provider,
            )

        # Vertex AI Text-to-Speech (Google Cloud TTS)
        if text_to_speech_provider_config is None:
            text_to_speech_provider_config = VertexAITextToSpeechConfig()

        # Cast to specific Vertex AI config type to access dispatch method
        vertex_config = cast(VertexAITextToSpeechConfig, text_to_speech_provider_config)

        # Store Vertex AI specific params in litellm_params_dict
        litellm_params_dict.update(
            {
                "vertex_project": generic_optional_params.vertex_project,
                "vertex_location": generic_optional_params.vertex_location,
                "vertex_credentials": generic_optional_params.vertex_credentials,
            }
        )

        response = vertex_config.dispatch_text_to_speech(
            model=model,
            input=input,
            voice=voice,
            optional_params=optional_params,
            litellm_params_dict=litellm_params_dict,
            logging_obj=logging_obj,
            timeout=timeout,
            extra_headers=headers,
            base_llm_http_handler=base_llm_http_handler,
            aspeech=aspeech or False,
            api_base=generic_optional_params.api_base,
            api_key=None,  # Vertex AI uses OAuth, not API key
            **kwargs,
        )
    elif custom_llm_provider == "gemini":
        from .endpoints.speech.speech_to_completion_bridge.handler import (
            speech_to_completion_bridge_handler,
        )

        return speech_to_completion_bridge_handler.speech(
            model=model,
            input=input,
            voice=voice,
            optional_params=optional_params,
            litellm_params=litellm_params_dict,
            headers=headers or {},
            logging_obj=logging_obj,
            custom_llm_provider=custom_llm_provider,
        )
    elif custom_llm_provider == "runwayml":
        from litellm.llms.runwayml.text_to_speech.transformation import (
            RunwayMLTextToSpeechConfig,
        )

        # RunwayML Text-to-Speech
        if text_to_speech_provider_config is None:
            raise litellm.BadRequestError(
                message="RunwayML Text-to-Speech configuration not found",
                model=model,
                llm_provider=custom_llm_provider,
            )

        # Cast to specific RunwayML config type to access dispatch method
        runwayml_config = cast(
            RunwayMLTextToSpeechConfig, text_to_speech_provider_config
        )

        response = runwayml_config.dispatch_text_to_speech(  # type: ignore
            model=model,
            input=input,
            voice=voice,
            optional_params=optional_params,
            litellm_params_dict=litellm_params_dict,
            logging_obj=logging_obj,
            timeout=timeout,
            extra_headers=extra_headers,
            base_llm_http_handler=base_llm_http_handler,
            aspeech=aspeech or False,
            api_base=api_base,
            api_key=api_key,
            **kwargs,
        )
    elif custom_llm_provider == "minimax":
        from litellm.llms.minimax.text_to_speech.transformation import (
            MinimaxTextToSpeechConfig,
        )

        # MiniMax Text-to-Speech
        if text_to_speech_provider_config is None:
            text_to_speech_provider_config = MinimaxTextToSpeechConfig()

        minimax_config = cast(MinimaxTextToSpeechConfig, text_to_speech_provider_config)

        if api_base is not None:
            litellm_params_dict["api_base"] = api_base
        if api_key is not None:
            litellm_params_dict["api_key"] = api_key

        # Convert voice to string if it's a dict (minimax handler expects Optional[str])
        voice_str: Optional[str] = None
        if isinstance(voice, str):
            voice_str = voice
        elif isinstance(voice, dict):
            # Extract voice_id from dict if needed
            voice_str = voice.get("voice_id") or voice.get("id") or voice.get("name")

        response = base_llm_http_handler.text_to_speech_handler(
            model=model,
            input=input,
            voice=voice_str,
            text_to_speech_provider_config=minimax_config,
            text_to_speech_optional_params=optional_params,
            custom_llm_provider=custom_llm_provider,
            litellm_params=litellm_params_dict,
            logging_obj=logging_obj,
            timeout=timeout,
            extra_headers=extra_headers,
            client=client,
            _is_async=aspeech or False,
        )
    elif custom_llm_provider == "aws_polly":
        from litellm.llms.aws_polly.text_to_speech.transformation import (
            AWSPollyTextToSpeechConfig,
        )

        # AWS Polly Text-to-Speech
        if text_to_speech_provider_config is None:
            text_to_speech_provider_config = AWSPollyTextToSpeechConfig()

        # Cast to specific AWS Polly config type to access dispatch method
        aws_polly_config = cast(
            AWSPollyTextToSpeechConfig, text_to_speech_provider_config
        )

        response = aws_polly_config.dispatch_text_to_speech(
            model=model,
            input=input,
            voice=voice,
            optional_params=optional_params,
            litellm_params_dict=litellm_params_dict,
            logging_obj=logging_obj,
            timeout=timeout,
            extra_headers=extra_headers,
            base_llm_http_handler=base_llm_http_handler,
            aspeech=aspeech or False,
            api_base=api_base,
            api_key=api_key,
            **kwargs,
        )

    if response is None:
        raise Exception(
            "Unable to map the custom llm provider={} to a known provider={}.".format(
                custom_llm_provider, litellm.provider_list
            )
        )
    return response

