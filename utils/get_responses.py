
def get_responses(
    response_id: str,
    # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
    # The extra values given here take precedence over values defined on the client or passed to this method.
    extra_headers: Optional[Dict[str, Any]] = None,
    extra_query: Optional[Dict[str, Any]] = None,
    extra_body: Optional[Dict[str, Any]] = None,
    timeout: Optional[Union[float, httpx.Timeout]] = None,
    # LiteLLM specific params,
    custom_llm_provider: Optional[str] = None,
    **kwargs,
) -> Union[ResponsesAPIResponse, Coroutine[Any, Any, ResponsesAPIResponse]]:
    """
    Fetch a response by its ID.

    GET /v1/responses/{response_id} endpoint in the responses API

    Args:
        response_id: The ID of the response to fetch.
        custom_llm_provider: Optional provider name. If not specified, will be decoded from response_id.

    Returns:
        The response object with complete information about the stored response.
    """
    local_vars = locals()
    try:
        litellm_logging_obj: LiteLLMLoggingObj = kwargs.get("litellm_logging_obj")  # type: ignore
        litellm_call_id: Optional[str] = kwargs.get("litellm_call_id", None)
        _is_async = kwargs.pop("aget_responses", False) is True

        # get llm provider logic
        litellm_params = GenericLiteLLMParams(**kwargs)

        # get custom llm provider from response_id
        decoded_response_id: DecodedResponseId = (
            ResponsesAPIRequestUtils._decode_responses_api_response_id(
                response_id=response_id,
            )
        )
        response_id = decoded_response_id.get("response_id") or response_id
        custom_llm_provider = (
            decoded_response_id.get("custom_llm_provider") or custom_llm_provider
        )

        if custom_llm_provider is None:
            raise ValueError("custom_llm_provider is required but passed as None")

        # get provider config
        responses_api_provider_config: Optional[BaseResponsesAPIConfig] = (
            ProviderConfigManager.get_provider_responses_api_config(
                model=None,
                provider=custom_llm_provider,
            )
        )

        if responses_api_provider_config is None:
            raise ValueError(
                f"GET responses is not supported for {custom_llm_provider}"
            )

        local_vars.update(kwargs)

        # Pre Call logging
        litellm_logging_obj.update_from_kwargs(
            kwargs=local_vars,
            model=None,
            optional_params={
                "response_id": response_id,
            },
            litellm_params={
                "litellm_call_id": litellm_call_id,
            },
            custom_llm_provider=custom_llm_provider,
        )

        # Call the handler with _is_async flag instead of directly calling the async handler
        response = base_llm_http_handler.get_responses(
            response_id=response_id,
            custom_llm_provider=custom_llm_provider,
            responses_api_provider_config=responses_api_provider_config,
            litellm_params=litellm_params,
            logging_obj=litellm_logging_obj,
            extra_headers=extra_headers,
            extra_body=extra_body,
            timeout=timeout or request_timeout,
            _is_async=_is_async,
            client=kwargs.get("client"),
            shared_session=kwargs.get("shared_session"),
        )

        # Update the responses_api_response_id with the model_id
        if isinstance(response, ResponsesAPIResponse):
            response = ResponsesAPIRequestUtils._update_responses_api_response_id_with_model_id(
                responses_api_response=response,
                litellm_metadata=kwargs.get("litellm_metadata", {}),
                custom_llm_provider=custom_llm_provider,
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

