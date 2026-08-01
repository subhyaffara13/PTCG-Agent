
def list_input_items(
    response_id: str,
    after: Optional[str] = None,
    before: Optional[str] = None,
    include: Optional[List[str]] = None,
    limit: int = 20,
    order: Literal["asc", "desc"] = "desc",
    extra_headers: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    custom_llm_provider: Optional[str] = None,
    **kwargs,
) -> Union[Dict, Coroutine[Any, Any, Dict]]:
    """List input items for a response"""
    local_vars = locals()
    try:
        litellm_logging_obj: LiteLLMLoggingObj = kwargs.get("litellm_logging_obj")  # type: ignore
        litellm_call_id: Optional[str] = kwargs.get("litellm_call_id", None)
        _is_async = kwargs.pop("alist_input_items", False) is True

        litellm_params = GenericLiteLLMParams(**kwargs)

        decoded_response_id = (
            ResponsesAPIRequestUtils._decode_responses_api_response_id(
                response_id=response_id
            )
        )
        response_id = decoded_response_id.get("response_id") or response_id
        custom_llm_provider = (
            decoded_response_id.get("custom_llm_provider") or custom_llm_provider
        )

        if custom_llm_provider is None:
            raise ValueError("custom_llm_provider is required but passed as None")

        responses_api_provider_config: Optional[BaseResponsesAPIConfig] = (
            ProviderConfigManager.get_provider_responses_api_config(
                model=None,
                provider=custom_llm_provider,
            )
        )

        if responses_api_provider_config is None:
            raise ValueError(
                f"list_input_items is not supported for {custom_llm_provider}"
            )

        local_vars.update(kwargs)

        litellm_logging_obj.update_from_kwargs(
            kwargs=local_vars,
            model=None,
            optional_params={"response_id": response_id},
            litellm_params={"litellm_call_id": litellm_call_id},
            custom_llm_provider=custom_llm_provider,
        )

        response = base_llm_http_handler.list_responses_input_items(
            response_id=response_id,
            custom_llm_provider=custom_llm_provider,
            responses_api_provider_config=responses_api_provider_config,
            litellm_params=litellm_params,
            logging_obj=litellm_logging_obj,
            after=after,
            before=before,
            include=include,
            limit=limit,
            order=order,
            extra_headers=extra_headers,
            timeout=timeout or request_timeout,
            _is_async=_is_async,
            client=kwargs.get("client"),
            shared_session=kwargs.get("shared_session"),
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

