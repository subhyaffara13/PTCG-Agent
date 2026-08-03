import json
from typing import Any, Dict, Optional, Union

def video_get_character(
    character_id: str,
    timeout=600,
    custom_llm_provider=None,
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    **kwargs,
) -> Union[CharacterObject, Coroutine[Any, Any, CharacterObject]]:
    """
    Retrieve a character by ID.
    Maps to GET /v1/videos/characters/{character_id}
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
            return CharacterObject(**mock_response)

        if custom_llm_provider is None:
            custom_llm_provider = "openai"

        litellm_params = GenericLiteLLMParams(**kwargs)

        provider_config: Optional[BaseVideoConfig] = (
            ProviderConfigManager.get_provider_video_config(
                model=None,
                provider=litellm.LlmProviders(custom_llm_provider),
            )
        )

        if provider_config is None:
            raise ValueError(
                f"video get character is not supported for {custom_llm_provider}"
            )

        local_vars.update(kwargs)
        request_params: Dict = {"character_id": character_id}

        litellm_logging_obj.update_environment_variables(
            model="",
            user=kwargs.get("user"),
            optional_params=dict(request_params),
            litellm_params={"litellm_call_id": litellm_call_id, **request_params},
            custom_llm_provider=custom_llm_provider,
        )

        litellm_logging_obj.call_type = CallTypes.video_get_character.value

        return base_llm_http_handler.video_get_character_handler(
            character_id=character_id,
            video_provider_config=provider_config,
            custom_llm_provider=custom_llm_provider,
            litellm_params=litellm_params,
            logging_obj=litellm_logging_obj,
            extra_headers=extra_headers,
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

