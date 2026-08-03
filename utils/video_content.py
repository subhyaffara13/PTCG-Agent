from typing import Any, Dict, Optional, Union

def video_content(
    video_id: str,
    timeout: Optional[float] = None,
    custom_llm_provider: Optional[str] = None,
    variant: Optional[str] = None,
    # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
    # The extra values given here take precedence over values defined on the client or passed to this method.
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    **kwargs,
) -> Union[
    bytes,
    Coroutine[Any, Any, bytes],
]:
    """
    Download video content from OpenAI's video API.

    Args:
        video_id (str): The identifier of the video whose content to download.
        api_key (Optional[str]): The API key to use for authentication.
        api_base (Optional[str]): The base URL for the API.
        timeout (Optional[float]): The timeout for the request in seconds.
        custom_llm_provider (Optional[str]): The LLM provider to use. If not provided, will be auto-detected.
        variant (Optional[str]): Which downloadable asset to return. Defaults to the MP4 video.
        extra_headers (Optional[Dict[str, Any]]): Additional headers to include in the request.
        extra_query (Optional[Dict[str, Any]]): Additional query parameters.
        extra_body (Optional[Dict[str, Any]]): Additional body parameters.

    Returns:
        bytes: The raw video content as bytes.

    Example:
        ```python
        import litellm

        video_bytes = litellm.video_content(
            video_id="video_123"
        )

        with open("video.mp4", "wb") as f:
            f.write(video_bytes)
        ```
    """
    local_vars = locals()
    try:
        litellm_logging_obj: LiteLLMLoggingObj = kwargs.get("litellm_logging_obj")  # type: ignore
        litellm_call_id: Optional[str] = kwargs.get("litellm_call_id", None)
        _is_async = kwargs.pop("async_call", False) is True

        # Try to decode provider from video_id if not explicitly provided
        if custom_llm_provider is None:
            decoded = decode_video_id_with_provider(video_id)
            custom_llm_provider = decoded.get("custom_llm_provider") or "openai"

        # get llm provider logic
        litellm_params = GenericLiteLLMParams(**kwargs)

        # get provider config
        video_provider_config: Optional[BaseVideoConfig] = (
            ProviderConfigManager.get_provider_video_config(
                model=None,
                provider=litellm.LlmProviders(custom_llm_provider),
            )
        )

        if video_provider_config is None:
            raise ValueError(
                f"video support download is not supported for {custom_llm_provider}"
            )

        local_vars.update(kwargs)
        # For video content download, we don't need complex optional parameter handling
        # Just pass the basic parameters that are relevant for content download
        video_content_request_params: Dict = {
            "video_id": video_id,
        }

        # Pre Call logging
        litellm_logging_obj.update_from_kwargs(
            kwargs=kwargs,
            model="",
            user=kwargs.get("user"),
            optional_params=dict(video_content_request_params),
            litellm_params={
                "litellm_call_id": litellm_call_id,
                **video_content_request_params,
            },
            custom_llm_provider=custom_llm_provider,
        )

        # Call the handler with _is_async flag instead of directly calling the async handler
        return base_llm_http_handler.video_content_handler(
            video_id=video_id,
            video_content_provider_config=video_provider_config,
            custom_llm_provider=custom_llm_provider,
            litellm_params=litellm_params,
            logging_obj=litellm_logging_obj,
            timeout=timeout or DEFAULT_REQUEST_TIMEOUT,
            extra_headers=extra_headers,
            client=kwargs.get("client"),
            _is_async=_is_async,
            variant=variant,
        )

    except Exception as e:
        raise litellm.exception_type(
            model="",
            custom_llm_provider=custom_llm_provider,
            original_exception=e,
            completion_kwargs=local_vars,
            extra_kwargs=kwargs,
        )

