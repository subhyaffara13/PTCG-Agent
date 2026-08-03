from typing import Optional

def image_variation(
    image: FileTypes,
    model: str = "dall-e-2",  # set to dall-e-2 by default - like OpenAI.
    n: int = 1,
    response_format: Literal["url", "b64_json"] = "url",
    size: Optional[str] = None,
    user: Optional[str] = None,
    **kwargs,
) -> ImageResponse:
    # get non-default params
    client = kwargs.get("client", None)
    # get logging object
    litellm_logging_obj = cast(LiteLLMLoggingObj, kwargs.get("litellm_logging_obj"))

    # get the litellm params
    litellm_params = get_litellm_params(**kwargs)
    # get the custom llm provider
    model, custom_llm_provider, dynamic_api_key, api_base = get_llm_provider(
        model=model,
        custom_llm_provider=litellm_params.get("custom_llm_provider", None),
        api_base=litellm_params.get("api_base", None),
        api_key=litellm_params.get("api_key", None),
    )

    # route to the correct provider w/ the params
    try:
        llm_provider = LlmProviders(custom_llm_provider)
        image_variation_provider = LITELLM_IMAGE_VARIATION_PROVIDERS(llm_provider)
    except ValueError:
        raise ValueError(
            f"Invalid image variation provider: {custom_llm_provider}. Supported providers are: {LITELLM_IMAGE_VARIATION_PROVIDERS}"
        )
    model_response = ImageResponse()

    response: Optional[ImageResponse] = None

    provider_config = ProviderConfigManager.get_provider_model_info(
        model=model or "",  # openai defaults to dall-e-2
        provider=llm_provider,
    )

    if provider_config is None:
        raise ValueError(
            f"image variation provider has no known model info config - required for getting api keys, etc.: {custom_llm_provider}. Supported providers are: {LITELLM_IMAGE_VARIATION_PROVIDERS}"
        )

    api_key = provider_config.get_api_key(litellm_params.get("api_key", None))
    api_base = provider_config.get_api_base(litellm_params.get("api_base", None))

    if image_variation_provider == LITELLM_IMAGE_VARIATION_PROVIDERS.OPENAI:
        if api_key is None:
            raise ValueError("API key is required for OpenAI image variations")
        if api_base is None:
            raise ValueError("API base is required for OpenAI image variations")

        response = openai_image_variations.image_variations(
            model_response=model_response,
            api_key=api_key,
            api_base=api_base,
            model=model,
            image=image,
            timeout=litellm_params.get("timeout", None),
            custom_llm_provider=custom_llm_provider,
            logging_obj=litellm_logging_obj,
            optional_params={},
            litellm_params=litellm_params,
        )
    elif image_variation_provider == LITELLM_IMAGE_VARIATION_PROVIDERS.TOPAZ:
        if api_key is None:
            raise ValueError("API key is required for Topaz image variations")
        if api_base is None:
            raise ValueError("API base is required for Topaz image variations")

        response = base_llm_aiohttp_handler.image_variations(
            model_response=model_response,
            api_key=api_key,
            api_base=api_base,
            model=model,
            image=image,
            timeout=litellm_params.get("timeout", None) or DEFAULT_REQUEST_TIMEOUT,
            custom_llm_provider=custom_llm_provider,
            logging_obj=litellm_logging_obj,
            optional_params={},
            litellm_params=litellm_params,
            client=client,
        )

    # return the response
    if response is None:
        raise ValueError(
            f"Invalid image variation provider: {custom_llm_provider}. Supported providers are: {LITELLM_IMAGE_VARIATION_PROVIDERS}"
        )
    return response

