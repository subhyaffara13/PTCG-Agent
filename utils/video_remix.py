
def video_remix(
    video_id: str,
    prompt: str,
    timeout: int = 600,
    custom_llm_provider: Optional[str] = None,
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    *,
    avideo_remix: Literal[True],
    **kwargs: Any,
) -> Coroutine[Any, Any, VideoObject]:
    ...


def video_remix(
    video_id: str,
    prompt: str,
    timeout: int = 600,
    custom_llm_provider: Optional[str] = None,
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    *,
    avideo_remix: Literal[False] = False,
    **kwargs: Any,
) -> VideoObject:
    ...


def video_remix(
    video_id: str,
    prompt: str,
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
    Maps the https://api.openai.com/v1/videos/{video_id}/remix endpoint.

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

        # Try to decode provider from video_id if not explicitly provided
        if custom_llm_provider is None:
            decoded = decode_video_id_with_provider(video_id)
            custom_llm_provider = decoded.get("custom_llm_provider") or "openai"

        # get llm provider logic
        litellm_params = GenericLiteLLMParams(**kwargs)

        # get provider config
        video_remix_provider_config: Optional[BaseVideoConfig] = (
            ProviderConfigManager.get_provider_video_config(
                model=None,
                provider=litellm.LlmProviders(custom_llm_provider),
            )
        )

        if video_remix_provider_config is None:
            raise ValueError(f"video remix is not supported for {custom_llm_provider}")

        local_vars.update(kwargs)
        # For video remix, we need the video_id and prompt
        video_remix_request_params: Dict = {
            "video_id": video_id,
            "prompt": prompt,
        }

        # Pre Call logging
        litellm_logging_obj.update_from_kwargs(
            kwargs=kwargs,
            model="",
            user=kwargs.get("user"),
            optional_params=dict(video_remix_request_params),
            litellm_params={
                "litellm_call_id": litellm_call_id,
                **video_remix_request_params,
            },
            custom_llm_provider=custom_llm_provider,
        )

        # Set the correct call type for video remix
        litellm_logging_obj.call_type = CallTypes.video_remix.value

        # Call the handler with _is_async flag instead of directly calling the async handler
        return base_llm_http_handler.video_remix_handler(
            video_id=video_id,
            prompt=prompt,
            video_remix_provider_config=video_remix_provider_config,
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
            model="",
            custom_llm_provider=custom_llm_provider,
            original_exception=e,
            completion_kwargs=local_vars,
            extra_kwargs=kwargs,
        )

