import json
from typing import Any, Dict, Optional, Union

def list_container_files(
    container_id: str,
    after: Optional[str] = None,
    limit: Optional[int] = None,
    order: Optional[str] = None,
    timeout=600,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    api_version: Optional[str] = None,
    custom_llm_provider: Literal["openai", "azure", "azure_text"] = "openai",
    *,
    alist_container_files: Literal[True],
    **kwargs,
) -> Coroutine[Any, Any, ContainerFileListResponse]:
    ...


def list_container_files(
    container_id: str,
    after: Optional[str] = None,
    limit: Optional[int] = None,
    order: Optional[str] = None,
    timeout=600,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    api_version: Optional[str] = None,
    custom_llm_provider: Literal["openai", "azure", "azure_text"] = "openai",
    *,
    alist_container_files: Literal[False] = False,
    **kwargs,
) -> ContainerFileListResponse:
    ...


def list_container_files(
    container_id: str,
    after: Optional[str] = None,
    limit: Optional[int] = None,
    order: Optional[str] = None,
    timeout=600,  # default to 10 minutes
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    api_version: Optional[str] = None,
    custom_llm_provider: Literal["openai", "azure", "azure_text"] = "openai",
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    **kwargs,
) -> Union[
    ContainerFileListResponse,
    Coroutine[Any, Any, ContainerFileListResponse],
]:
    """List files in a container using the OpenAI Container API.

    Currently supports OpenAI
    """
    local_vars = locals()
    try:
        resolved_custom_llm_provider: str = custom_llm_provider
        litellm_logging_obj: LiteLLMLoggingObj = kwargs.pop("litellm_logging_obj")  # type: ignore
        litellm_call_id: Optional[str] = kwargs.get("litellm_call_id")
        _is_async = kwargs.pop("async_call", False) is True

        # Check for mock response first
        mock_response = kwargs.get("mock_response")
        if mock_response is not None:
            if isinstance(mock_response, str):
                mock_response = json.loads(mock_response)

            response = ContainerFileListResponse(**mock_response)
            return response

        # get llm provider logic
        # Pass credential params explicitly since they're named args, not in kwargs
        litellm_params = GenericLiteLLMParams(
            api_key=api_key,
            api_base=api_base,
            api_version=api_version,
            **kwargs,
        )

        # Decode container ID and extract provider info
        original_container_id, resolved_custom_llm_provider, litellm_params = (
            decode_managed_container_id_for_request(
                container_id=container_id,
                custom_llm_provider=custom_llm_provider,
                litellm_params=litellm_params,
            )
        )

        # get provider config
        container_provider_config: Optional[BaseContainerConfig] = (
            ProviderConfigManager.get_provider_container_config(
                provider=litellm.LlmProviders(resolved_custom_llm_provider),
            )
        )

        if container_provider_config is None:
            raise ValueError(
                f"Container provider config not found for provider: {resolved_custom_llm_provider}"
            )

        # Pre Call logging
        litellm_logging_obj.update_from_kwargs(
            kwargs=kwargs,
            model="",
            optional_params={
                "container_id": container_id,
                "after": after,
                "limit": limit,
                "order": order,
            },
            litellm_params={
                "litellm_call_id": litellm_call_id,
            },
            custom_llm_provider=resolved_custom_llm_provider,
        )

        # Set the correct call type
        litellm_logging_obj.call_type = CallTypes.list_container_files.value

        return base_llm_http_handler.container_file_list_handler(
            container_id=original_container_id,  # Use decoded original ID
            container_provider_config=container_provider_config,
            litellm_params=litellm_params,
            logging_obj=litellm_logging_obj,
            after=after,
            limit=limit,
            order=order,
            extra_headers=extra_headers,
            extra_query=extra_query,
            timeout=timeout or DEFAULT_REQUEST_TIMEOUT,
            _is_async=_is_async,
        )

    except Exception as e:
        raise litellm.exception_type(
            model="",
            custom_llm_provider=resolved_custom_llm_provider,
            original_exception=e,
            completion_kwargs=local_vars,
            extra_kwargs=kwargs,
        )

