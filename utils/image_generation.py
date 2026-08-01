
def image_generation(
    prompt: str,
    model: Optional[str] = None,
    n: Optional[int] = None,
    quality: Optional[Union[str, ImageGenerationRequestQuality]] = None,
    response_format: Optional[str] = None,
    size: Optional[str] = None,
    style: Optional[str] = None,
    user: Optional[str] = None,
    timeout=600,  # default to 10 minutes
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    api_version: Optional[str] = None,
    custom_llm_provider=None,
    *,
    aimg_generation: Literal[True],
    **kwargs,
) -> Coroutine[Any, Any, ImageResponse]: 
    ...


def image_generation(
    prompt: str,
    model: Optional[str] = None,
    n: Optional[int] = None,
    quality: Optional[Union[str, ImageGenerationRequestQuality]] = None,
    response_format: Optional[str] = None,
    size: Optional[str] = None,
    style: Optional[str] = None,
    user: Optional[str] = None,
    timeout=600,  # default to 10 minutes
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    api_version: Optional[str] = None,
    custom_llm_provider=None,
    *,
    aimg_generation: Literal[False] = False,
    **kwargs,
) -> ImageResponse: 
    ...


def image_generation(
    prompt: str,
    model: Optional[str] = None,
    n: Optional[int] = None,
    quality: Optional[Union[str, ImageGenerationRequestQuality]] = None,
    response_format: Optional[str] = None,
    size: Optional[str] = None,
    style: Optional[str] = None,
    user: Optional[str] = None,
    timeout=600,  # default to 10 minutes
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    api_version: Optional[str] = None,
    custom_llm_provider=None,
    **kwargs,
) -> Union[
    ImageResponse,
    Coroutine[Any, Any, ImageResponse],
]:
    """
    Maps the https://api.openai.com/v1/images/generations endpoint.

    Currently supports just Azure + OpenAI.
    """
    try:
        args = locals()
        aimg_generation = kwargs.get("aimg_generation", False)
        litellm_call_id = kwargs.get("litellm_call_id", None)
        logger_fn = kwargs.get("logger_fn", None)
        mock_response: Optional[str] = kwargs.get("mock_response", None)  # type: ignore
        proxy_server_request = kwargs.get("proxy_server_request", None)
        azure_ad_token_provider = kwargs.get("azure_ad_token_provider", None)
        model_info = kwargs.get("model_info", None)
        metadata = kwargs.get("metadata", {})
        litellm_logging_obj: LiteLLMLoggingObj = kwargs.get("litellm_logging_obj")  # type: ignore
        client = kwargs.get("client", None)
        extra_headers = kwargs.get("extra_headers", None)
        headers: dict = kwargs.get("headers", None) or {}
        base_model = kwargs.get("base_model", None)
        if extra_headers is not None:
            headers.update(extra_headers)
        model_response: ImageResponse = litellm.utils.ImageResponse()
        dynamic_api_key: Optional[str] = None
        if model is not None or custom_llm_provider is not None:
            model, custom_llm_provider, dynamic_api_key, api_base = get_llm_provider(
                model=model,  # type: ignore
                custom_llm_provider=custom_llm_provider,
                api_base=api_base,
            )
        else:
            model = "dall-e-2"
            custom_llm_provider = "openai"  # default to dall-e-2 on openai
        model_response._hidden_params["model"] = model
        openai_params = [
            "user",
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
            "n",
            "quality",
            "size",
            "style",
        ]
        litellm_params = all_litellm_params
        default_params = openai_params + litellm_params
        non_default_params = {
            k: v for k, v in kwargs.items() if k not in default_params
        }  # model-specific params - pass them straight to the model/provider

        image_generation_config: Optional[BaseImageGenerationConfig] = None
        if (
            custom_llm_provider is not None
            and custom_llm_provider in LlmProviders._member_map_.values()
        ):
            image_generation_config = (
                ProviderConfigManager.get_provider_image_generation_config(
                    model=base_model or model,
                    provider=LlmProviders(custom_llm_provider),
                )
            )

        optional_params = get_optional_params_image_gen(
            model=base_model or model,
            n=n,
            quality=quality,
            response_format=response_format,
            size=size,
            style=style,
            user=user,
            custom_llm_provider=custom_llm_provider,
            provider_config=image_generation_config,
            **non_default_params,
        )

        litellm_params_dict = get_litellm_params(**kwargs)

        logging: Logging = litellm_logging_obj
        logging.update_from_kwargs(
            kwargs=kwargs,
            model=model,
            user=user,
            optional_params=optional_params,
            litellm_params={
                "timeout": timeout,
                "azure": False,
                "litellm_call_id": litellm_call_id,
                "logger_fn": logger_fn,
                "proxy_server_request": proxy_server_request,
                "model_info": model_info,
                "preset_cache_key": None,
                "stream_response": {},
            },
            custom_llm_provider=custom_llm_provider,
        )
        if "custom_llm_provider" not in logging.model_call_details:
            logging.model_call_details["custom_llm_provider"] = custom_llm_provider
        if mock_response is not None:
            return mock_image_generation(model=model, mock_response=mock_response)

        if custom_llm_provider == "azure":
            # azure configs
            api_type = get_secret_str("AZURE_API_TYPE") or "azure"

            api_base = api_base or litellm.api_base or get_secret_str("AZURE_API_BASE")

            api_version = (
                api_version
                or litellm.api_version
                or get_secret_str("AZURE_API_VERSION")
            )

            api_key = (
                api_key
                or litellm.api_key
                or litellm.azure_key
                or get_secret_str("AZURE_OPENAI_API_KEY")
                or get_secret_str("AZURE_API_KEY")
            )

            azure_ad_token = optional_params.pop(
                "azure_ad_token", None
            ) or get_secret_str("AZURE_AD_TOKEN")

            # Create azure_ad_token_provider from tenant_id, client_id, client_secret if not already provided
            if azure_ad_token_provider is None:
                from litellm.llms.azure.common_utils import (
                    get_azure_ad_token_from_entra_id,
                )

                # Extract Azure AD credentials from litellm_params
                tenant_id = litellm_params_dict.get("tenant_id")
                client_id = litellm_params_dict.get("client_id")
                client_secret = litellm_params_dict.get("client_secret")
                azure_scope = (
                    litellm_params_dict.get("azure_scope")
                    or "https://cognitiveservices.azure.com/.default"
                )

                # Create token provider if credentials are available
                if tenant_id and client_id and client_secret:
                    azure_ad_token_provider = get_azure_ad_token_from_entra_id(
                        tenant_id=tenant_id,
                        client_id=client_id,
                        client_secret=client_secret,
                        scope=azure_scope,
                    )

            default_headers = {
                "Content-Type": "application/json",
            }
            # Only add api-key header if api_key is not None
            # Azure AD authentication will use Authorization header instead
            if api_key is not None:
                default_headers["api-key"] = api_key

            for k, v in default_headers.items():
                if k not in headers:
                    headers[k] = v

            model_response = azure_chat_completions.image_generation(
                model=model,
                prompt=prompt,
                timeout=timeout,
                api_key=api_key,
                api_base=api_base,
                azure_ad_token=azure_ad_token,
                azure_ad_token_provider=azure_ad_token_provider,
                logging_obj=litellm_logging_obj,
                optional_params=optional_params,
                model_response=model_response,
                api_version=api_version,
                aimg_generation=aimg_generation,
                client=client,
                headers=headers,
                litellm_params=litellm_params_dict,
            )
        #########################################################
        # Providers using llm_http_handler
        #########################################################
        elif custom_llm_provider in (
            litellm.LlmProviders.RECRAFT,
            litellm.LlmProviders.AIML,
            litellm.LlmProviders.GEMINI,
            litellm.LlmProviders.FAL_AI,
            litellm.LlmProviders.STABILITY,
            litellm.LlmProviders.RUNWAYML,
            litellm.LlmProviders.VERTEX_AI,
            litellm.LlmProviders.OPENROUTER,
            litellm.LlmProviders.DASHSCOPE,
        ):
            if image_generation_config is None:
                raise ValueError(
                    f"image generation config is not supported for {custom_llm_provider}"
                )

            # Resolve api_base from litellm.api_base if not explicitly provided
            _api_base = api_base or litellm.api_base
            litellm_params_dict["api_base"] = _api_base

            return llm_http_handler.image_generation_handler(
                api_key=api_key,
                model=model,
                prompt=prompt,
                image_generation_provider_config=image_generation_config,
                image_generation_optional_request_params=optional_params,
                custom_llm_provider=custom_llm_provider,
                litellm_params=litellm_params_dict,
                logging_obj=litellm_logging_obj,
                timeout=timeout,
                client=client,
            )
        elif custom_llm_provider == "black_forest_labs":
            # Route to BFL-specific handler (polling required)
            if model is None:
                raise Exception("Model needs to be set for black_forest_labs")
            return bfl_image_generation.image_generation(
                model=model,
                prompt=prompt,
                model_response=model_response,
                optional_params=optional_params,
                litellm_params=litellm_params_dict,
                logging_obj=litellm_logging_obj,
                timeout=timeout,
                extra_headers=extra_headers,
                client=client,
                aimg_generation=aimg_generation,
            )
        elif custom_llm_provider == "azure_ai":
            from litellm.llms.azure_ai.common_utils import AzureFoundryModelInfo

            api_base = AzureFoundryModelInfo.get_api_base(api_base)
            api_key = AzureFoundryModelInfo.get_api_key(api_key)
            if extra_headers is not None:
                optional_params["extra_headers"] = extra_headers

            default_headers = {
                "Content-Type": "application/json",
            }
            # Only add api-key header if api_key is not None
            # Azure AD authentication will use Authorization header instead
            if api_key is not None:
                default_headers["api-key"] = api_key

            for k, v in default_headers.items():
                if k not in headers:
                    headers[k] = v

            model_response = azure_chat_completions.image_generation(
                model=model,
                prompt=prompt,
                timeout=timeout,
                api_key=api_key,
                api_base=api_base,
                azure_ad_token=None,
                azure_ad_token_provider=azure_ad_token_provider,
                logging_obj=litellm_logging_obj,
                optional_params=optional_params,
                model_response=model_response,
                api_version=api_version,
                aimg_generation=aimg_generation,
                client=client,
                headers=headers,
                litellm_params=litellm_params_dict,
            )
        elif (
            custom_llm_provider == "openai"
            or custom_llm_provider == LlmProviders.LITELLM_PROXY.value
            or custom_llm_provider in litellm.openai_compatible_providers
        ):
            if extra_headers is not None:
                optional_params["extra_headers"] = extra_headers
            # Forward OpenAI organization if present (set by proxy pre-call utils)
            organization: Optional[str] = kwargs.get("organization", None)
            model_response = openai_chat_completions.image_generation(
                model=model,
                prompt=prompt,
                timeout=timeout,
                api_key=api_key or dynamic_api_key,
                api_base=api_base,
                logging_obj=litellm_logging_obj,
                optional_params=optional_params,
                model_response=model_response,
                organization=organization,
                aimg_generation=aimg_generation,
                client=client,
                headers=headers,
            )
        elif custom_llm_provider == "bedrock":
            if model is None:
                raise Exception("Model needs to be set for bedrock")
            model_response = bedrock_image_generation.image_generation(  # type: ignore
                model=model,
                prompt=prompt,
                timeout=timeout,
                logging_obj=litellm_logging_obj,
                optional_params=optional_params,
                model_response=model_response,
                aimg_generation=aimg_generation,
                client=client,
                api_base=api_base,
                api_key=api_key,
            )
        elif (
            custom_llm_provider in litellm._custom_providers
        ):  # Assume custom LLM provider
            # Get the Custom Handler
            custom_handler: Optional[CustomLLM] = None
            for item in litellm.custom_provider_map:
                if item["provider"] == custom_llm_provider:
                    custom_handler = item["custom_handler"]

            if custom_handler is None:
                raise LiteLLMUnknownProvider(
                    model=model, custom_llm_provider=custom_llm_provider
                )

            ## ROUTE LLM CALL ##
            if aimg_generation is True:
                async_custom_client: Optional[AsyncHTTPHandler] = None
                if client is not None and isinstance(client, AsyncHTTPHandler):
                    async_custom_client = client

                ## CALL FUNCTION
                model_response = custom_handler.aimage_generation(  # type: ignore
                    model=model,
                    prompt=prompt,
                    api_key=api_key,
                    api_base=api_base,
                    model_response=model_response,
                    optional_params=optional_params,
                    logging_obj=litellm_logging_obj,
                    timeout=timeout,
                    client=async_custom_client,
                )
            else:
                custom_client: Optional[HTTPHandler] = None
                if client is not None and isinstance(client, HTTPHandler):
                    custom_client = client

                ## CALL FUNCTION
                model_response = custom_handler.image_generation(
                    model=model,
                    prompt=prompt,
                    api_key=api_key,
                    api_base=api_base,
                    model_response=model_response,
                    optional_params=optional_params,
                    logging_obj=litellm_logging_obj,
                    timeout=timeout,
                    client=custom_client,
                )

        return model_response
    except Exception as e:
        ## Map to OpenAI Exception
        raise exception_type(
            model=model,
            custom_llm_provider=custom_llm_provider,
            original_exception=e,
            completion_kwargs=locals(),
            extra_kwargs=kwargs,
        )

