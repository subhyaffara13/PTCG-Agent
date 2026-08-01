
def video_generation(
    prompt: str,
    model: Optional[str] = None,
    input_reference: Optional[FileTypes] = None,
    seconds: Optional[str] = None,
    size: Optional[str] = None,
    user: Optional[str] = None,
    timeout: int = 600,
    custom_llm_provider: Optional[str] = None,
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    *,
    avideo_generation: Literal[True],
    **kwargs: Any,
) -> Coroutine[Any, Any, VideoObject]:
    ...


def video_generation(
    prompt: str,
    model: Optional[str] = None,
    input_reference: Optional[FileTypes] = None,
    seconds: Optional[str] = None,
    size: Optional[str] = None,
    user: Optional[str] = None,
    timeout: int = 600,
    custom_llm_provider: Optional[str] = None,
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    *,
    avideo_generation: Literal[False] = False,
    **kwargs: Any,
) -> VideoObject:
    ...


def video_generation(
    prompt: str,
    model: Optional[str] = None,
    input_reference: Optional[FileTypes] = None,
    seconds: Optional[str] = None,
    size: Optional[str] = None,
    user: Optional[str] = None,
    timeout=600,  # default to 10 minutes
    custom_llm_provider=None,
    # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
    # The extra values given here take precedence over values defined on the client or passed to this method.
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    **kwargs,
) -> Union[
    VideoObject,
    Coroutine[Any, Any, VideoObject],
]:
    """
    Maps the https://api.openai.com/v1/videos endpoint.

    Currently supports OpenAI
    """
    local_vars = locals()
    try:
        litellm_logging_obj: LiteLLMLoggingObj = kwargs.pop("litellm_logging_obj")  # type: ignore
        litellm_call_id: Optional[str] = kwargs.get("litellm_call_id", None)
        _is_async = kwargs.pop("async_call", False) is True

        # Check for mock response first
        mock_response = kwargs.get("mock_response", None)
        if mock_response is not None:
            if isinstance(mock_response, str):
                mock_response = json.loads(mock_response)

            response = VideoObject(**mock_response)
            return response

        # get llm provider logic
        litellm_params = GenericLiteLLMParams(**kwargs)
        model, custom_llm_provider, _, _ = get_llm_provider(
            model=model or DEFAULT_VIDEO_ENDPOINT_MODEL,
            custom_llm_provider=custom_llm_provider,
        )

        # get provider config
        video_generation_provider_config: Optional[BaseVideoConfig] = (
            ProviderConfigManager.get_provider_video_config(
                model=model,
                provider=litellm.LlmProviders(custom_llm_provider),
            )
        )

        if video_generation_provider_config is None:
            raise ValueError(
                f"video generation is not supported for {custom_llm_provider}"
            )

        local_vars.update(kwargs)
        # Get VideoGenerationOptionalRequestParams with only valid parameters
        video_generation_optional_params: VideoCreateOptionalRequestParams = (
            VideoGenerationRequestUtils.get_requested_video_generation_optional_param(
                local_vars
            )
        )

        # Get optional parameters for the video generation API
        video_generation_request_params: Dict = (
            VideoGenerationRequestUtils.get_optional_params_video_generation(
                model=model,
                video_generation_provider_config=video_generation_provider_config,
                video_generation_optional_params=video_generation_optional_params,
            )
        )

        # Pre Call logging
        litellm_logging_obj.update_from_kwargs(
            kwargs=kwargs,
            model=model,
            user=user,
            optional_params=dict(video_generation_request_params),
            litellm_params={
                "litellm_call_id": litellm_call_id,
                **video_generation_request_params,
            },
            custom_llm_provider=custom_llm_provider,
        )

        # Set the correct call type for video generation
        litellm_logging_obj.call_type = CallTypes.create_video.value

        # Call the handler with _is_async flag instead of directly calling the async handler
        return base_llm_http_handler.video_generation_handler(
            model=model,
            prompt=prompt,
            video_generation_provider_config=video_generation_provider_config,
            video_generation_optional_request_params=video_generation_request_params,
            custom_llm_provider=custom_llm_provider,
            litellm_params=litellm_params,
            logging_obj=litellm_logging_obj,
            extra_headers=extra_headers,
            extra_body=extra_body,
            timeout=timeout or DEFAULT_REQUEST_TIMEOUT,
            _is_async=_is_async,
            client=kwargs.get("client"),
        )

    except Exception as e:
        raise litellm.exception_type(
            model=model or DEFAULT_VIDEO_ENDPOINT_MODEL,
            custom_llm_provider=custom_llm_provider,
            original_exception=e,
            completion_kwargs=local_vars,
            extra_kwargs=kwargs,
        )

