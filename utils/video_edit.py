
def video_edit(
    video_id: str,
    prompt: str,
    timeout=600,
    custom_llm_provider=None,
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    **kwargs,
) -> Union[VideoObject, Coroutine[Any, Any, VideoObject]]:
    """
    Create a video edit job.
    Maps to POST /v1/videos/edits
    """
    local_vars = locals()
    try:
        litellm_logging_obj: LiteLLMLoggingObj = kwargs.pop("litellm_logging_obj")  # type: ignore
        litellm_call_id: Optional[str] = kwargs.get("litellm_call_id", None)
        _is_async = kwargs.pop("async_call", False) is True

        mock_response = kwargs.get("mock_response", None)
        if mock_response is not None:
            if isinstance(mock_response, str):
                mock_response = json.loads(mock_response)
            return VideoObject(**mock_response)

        if custom_llm_provider is None:
            decoded = decode_video_id_with_provider(video_id)
            custom_llm_provider = decoded.get("custom_llm_provider") or "openai"

        litellm_params = GenericLiteLLMParams(**kwargs)

        provider_config: Optional[BaseVideoConfig] = (
            ProviderConfigManager.get_provider_video_config(
                model=None,
                provider=litellm.LlmProviders(custom_llm_provider),
            )
        )

        if provider_config is None:
            raise ValueError(f"video edit is not supported for {custom_llm_provider}")

        local_vars.update(kwargs)
        request_params: Dict = {"video_id": video_id, "prompt": prompt}

        litellm_logging_obj.update_environment_variables(
            model="",
            user=kwargs.get("user"),
            optional_params=dict(request_params),
            litellm_params={"litellm_call_id": litellm_call_id, **request_params},
            custom_llm_provider=custom_llm_provider,
        )

        litellm_logging_obj.call_type = CallTypes.video_edit.value

        return base_llm_http_handler.video_edit_handler(
            prompt=prompt,
            video_id=video_id,
            video_provider_config=provider_config,
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

