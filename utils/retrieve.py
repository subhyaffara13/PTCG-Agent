from typing import Any, Dict, Optional, Union

def retrieve(
    vector_store_id: str,
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    custom_llm_provider: Optional[str] = None,
    **kwargs,
) -> Union[VectorStoreCreateResponse, Coroutine[Any, Any, VectorStoreCreateResponse]]:
    """
    Retrieve a vector store.

    Args:
        vector_store_id: The ID of the vector store to retrieve.

    Returns:
        VectorStoreCreateResponse containing the vector store details.
    """
    local_vars = locals()
    try:
        litellm_logging_obj: LiteLLMLoggingObj = kwargs.get("litellm_logging_obj")  # type: ignore
        litellm_call_id: Optional[str] = kwargs.get("litellm_call_id", None)
        _is_async = kwargs.pop("aretrieve", False) is True

        litellm_params = GenericLiteLLMParams(**kwargs)

        if custom_llm_provider is None:
            custom_llm_provider = "openai"

        if "/" in custom_llm_provider:
            api_type, custom_llm_provider, _, _ = get_llm_provider(
                model=custom_llm_provider,
                custom_llm_provider=None,
                litellm_params=None,
            )
        else:
            api_type = None
            custom_llm_provider = custom_llm_provider

        vector_store_provider_config = (
            ProviderConfigManager.get_provider_vector_stores_config(
                provider=litellm.LlmProviders(custom_llm_provider),
                api_type=api_type,
            )
        )

        if vector_store_provider_config is None:
            raise ValueError(
                f"Vector store retrieve is not supported for {custom_llm_provider}"
            )

        litellm_logging_obj.update_from_kwargs(
            kwargs=kwargs,
            model=None,
            optional_params={"vector_store_id": vector_store_id},
            litellm_params={"litellm_call_id": litellm_call_id},
            custom_llm_provider=custom_llm_provider,
        )

        response = base_llm_http_handler.vector_store_retrieve_handler(
            vector_store_id=vector_store_id,
            vector_store_provider_config=vector_store_provider_config,
            custom_llm_provider=custom_llm_provider,
            litellm_params=litellm_params,
            logging_obj=litellm_logging_obj,
            extra_headers=extra_headers,
            extra_body=extra_body,
            timeout=timeout or request_timeout,
            _is_async=_is_async,
            client=kwargs.get("client"),
        )

        return response
    except Exception as e:
        raise litellm.exception_type(
            model=None,
            custom_llm_provider=custom_llm_provider,
            original_exception=e,
            completion_kwargs=local_vars,
            extra_kwargs=kwargs,
        )


def retrieve(
    *,
    vector_store_id: str,
    file_id: str,
    extra_headers: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    custom_llm_provider: Optional[str] = None,
    **kwargs,
) -> Union[VectorStoreFileObject, Coroutine[Any, Any, VectorStoreFileObject]]:
    local_vars = locals()
    try:
        litellm_logging_obj: LiteLLMLoggingObj = kwargs.get("litellm_logging_obj")  # type: ignore
        litellm_call_id: Optional[str] = kwargs.get("litellm_call_id")
        _is_async = kwargs.pop("aretrieve", False) is True

        custom_llm_provider = _ensure_provider(custom_llm_provider)

        _prepare_registry_credentials(vector_store_id=vector_store_id, kwargs=kwargs)

        litellm_params = GenericLiteLLMParams(vector_store_id=vector_store_id, **kwargs)

        provider_config = ProviderConfigManager.get_provider_vector_store_files_config(
            provider=LlmProviders(custom_llm_provider)
        )
        if provider_config is None:
            raise ValueError(
                f"Vector store file retrieve is not supported for {custom_llm_provider}"
            )

        litellm_logging_obj.update_from_kwargs(
            kwargs=kwargs,
            model=None,
            optional_params={
                "vector_store_id": vector_store_id,
                "file_id": file_id,
            },
            litellm_params={
                "vector_store_id": vector_store_id,
                "litellm_call_id": litellm_call_id,
                **litellm_params.model_dump(exclude_none=True),
            },
            custom_llm_provider=custom_llm_provider,
        )

        response = base_llm_http_handler.vector_store_file_retrieve_handler(
            vector_store_id=vector_store_id,
            file_id=file_id,
            vector_store_files_provider_config=provider_config,
            custom_llm_provider=custom_llm_provider,
            litellm_params=litellm_params,
            logging_obj=litellm_logging_obj,
            extra_headers=extra_headers,
            timeout=timeout or request_timeout,
            client=kwargs.get("client"),
            _is_async=_is_async,
        )
        return response
    except Exception as e:  # noqa: BLE001
        raise litellm.exception_type(
            model=None,
            custom_llm_provider=custom_llm_provider,
            original_exception=e,
            completion_kwargs=local_vars,
            extra_kwargs=kwargs,
        )

