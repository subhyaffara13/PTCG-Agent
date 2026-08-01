
def compact_responses(
    input: Union[str, ResponseInputParam],
    model: str,
    instructions: Optional[str] = None,
    previous_response_id: Optional[str] = None,
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
    Synchronous version of the POST Compact Responses API

    POST /v1/responses/compact endpoint in the responses API

    Runs a compaction pass over a conversation, returning encrypted, opaque items.
    """
    local_vars = locals()
    try:
        litellm_logging_obj: LiteLLMLoggingObj = kwargs.get("litellm_logging_obj")  # type: ignore
        litellm_call_id: Optional[str] = kwargs.get("litellm_call_id", None)
        _is_async = kwargs.pop("acompact_responses", False) is True

        # get llm provider logic
        litellm_params = GenericLiteLLMParams(**kwargs)

        model, custom_llm_provider = _resolve_model_provider_for_responses(
            model=model,
            custom_llm_provider=custom_llm_provider,
            litellm_params=litellm_params,
            local_vars=local_vars,
        )

        if custom_llm_provider is None:
            raise ValueError("custom_llm_provider is required but passed as None")

        # get provider config
        responses_api_provider_config: Optional[BaseResponsesAPIConfig] = (
            ProviderConfigManager.get_provider_responses_api_config(
                model=model,
                provider=custom_llm_provider,
            )
        )

        if responses_api_provider_config is None:
            raise ValueError(
                f"COMPACT responses is not supported for {custom_llm_provider}"
            )

        local_vars.update(kwargs)

        # Build optional params for compact endpoint
        response_api_optional_params: ResponsesAPIOptionalRequestParams = (
            ResponsesAPIRequestUtils.get_requested_response_api_optional_param(
                local_vars
            )
        )

        # Get optional parameters for the responses API
        responses_api_request_params: Dict = (
            ResponsesAPIRequestUtils.get_optional_params_responses_api(
                model=model,
                responses_api_provider_config=responses_api_provider_config,
                response_api_optional_params=response_api_optional_params,
                allowed_openai_params=None,
            )
        )

        # Pre Call logging
        litellm_logging_obj.update_from_kwargs(
            kwargs=local_vars,
            model=model,
            optional_params=dict(responses_api_request_params),
            litellm_params={
                **responses_api_request_params,
                "litellm_call_id": litellm_call_id,
                "data_residency": infer_openai_data_residency(
                    custom_llm_provider, litellm_params.api_base
                ),
            },
            custom_llm_provider=custom_llm_provider,
        )

        # Decode any litellm-encoded encrypted-content item IDs back to their original IDs
        # before forwarding to the upstream provider.
        input = ResponsesAPIRequestUtils._restore_encrypted_content_item_ids_in_input(
            input
        )

        # Call the handler with _is_async flag instead of directly calling the async handler
        response = base_llm_http_handler.compact_response_api_handler(
            model=model,
            input=input,
            responses_api_provider_config=responses_api_provider_config,
            response_api_optional_request_params=responses_api_request_params,
            litellm_params=litellm_params,
            logging_obj=litellm_logging_obj,
            custom_llm_provider=custom_llm_provider,
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
            model=model,
            custom_llm_provider=custom_llm_provider,
            original_exception=e,
            completion_kwargs=local_vars,
            extra_kwargs=kwargs,
        )

