
def anthropic_messages_handler(
    max_tokens: int,
    messages: List[Dict],
    model: str,
    metadata: Optional[Dict] = None,
    stop_sequences: Optional[List[str]] = None,
    stream: Optional[bool] = False,
    system: Optional[str] = None,
    temperature: Optional[float] = None,
    thinking: Optional[Dict] = None,
    tool_choice: Optional[Dict] = None,
    tools: Optional[List[Dict]] = None,
    top_k: Optional[int] = None,
    top_p: Optional[float] = None,
    container: Optional[Dict] = None,
    api_key: Optional[str] = None,
    api_base: Optional[str] = None,
    client: Optional[AsyncHTTPHandler] = None,
    custom_llm_provider: Optional[str] = None,
    **kwargs,
) -> Union[
    AnthropicMessagesResponse,
    Iterator[bytes],
    AsyncIterator[Any],
    Coroutine[
        Any, Any, Union[AnthropicMessagesResponse, AsyncIterator[Any], Iterator[bytes]]
    ],
]:
    """
    Makes Anthropic `/v1/messages` API calls In the Anthropic API Spec

    Args:
        container: Container config with skills for code execution
    """
    from litellm.types.utils import LlmProviders

    # Sanitize empty text blocks so the sync entry point
    # (litellm.messages.create -> anthropic_messages_handler) gets the same
    # protection as the async wrapper. The async wrapper already sanitized and
    # does not reassign messages before dispatch, so it sets
    # ``_litellm_messages_presanitized`` to skip this redundant second
    # full-messages scan. Pop it so it never leaks into provider params.
    if not kwargs.pop("_litellm_messages_presanitized", False):
        messages = strip_empty_text_blocks_from_anthropic_messages(messages)

    metadata = validate_anthropic_api_metadata(metadata)

    local_vars = locals()
    is_async = kwargs.pop("is_async", False)
    # Use provided client or create a new one
    litellm_logging_obj: LiteLLMLoggingObj = kwargs.get("litellm_logging_obj")  # type: ignore

    # Store original model name before get_llm_provider strips the provider prefix
    # This is needed by agentic hooks (e.g., websearch_interception) to make follow-up requests
    original_model = model

    litellm_params = GenericLiteLLMParams(
        **kwargs,
        api_key=api_key,
        api_base=api_base,
        custom_llm_provider=custom_llm_provider,
    )
    (
        model,
        custom_llm_provider,
        dynamic_api_key,
        dynamic_api_base,
    ) = litellm.get_llm_provider(
        model=model,
        custom_llm_provider=custom_llm_provider,
        api_base=litellm_params.api_base,
        api_key=litellm_params.api_key,
    )

    # Store agentic loop params in logging object for agentic hooks
    # This provides original request context needed for follow-up calls
    if litellm_logging_obj is not None:
        litellm_logging_obj.model_call_details["agentic_loop_params"] = {
            "model": original_model,
            "custom_llm_provider": custom_llm_provider,
        }

        # Check if stream was converted for WebSearch interception
        # This is set in the async wrapper above when stream=True is converted to stream=False
        if kwargs.get("_websearch_interception_converted_stream", False):
            litellm_logging_obj.model_call_details[
                "websearch_interception_converted_stream"
            ] = True

    if litellm_params.mock_response and isinstance(litellm_params.mock_response, str):
        return mock_response(
            model=model,
            messages=messages,
            max_tokens=max_tokens,
            mock_response=litellm_params.mock_response,
        )

    anthropic_messages_provider_config: Optional[BaseAnthropicMessagesConfig] = None

    if custom_llm_provider is not None and custom_llm_provider in [
        provider.value for provider in LlmProviders
    ]:
        anthropic_messages_provider_config = (
            ProviderConfigManager.get_provider_anthropic_messages_config(
                model=model,
                provider=litellm.LlmProviders(custom_llm_provider),
            )
        )
    if anthropic_messages_provider_config is None:
        # Route to Responses API for OpenAI / Azure, chat/completions for everything else.
        _shared_kwargs = dict(
            max_tokens=max_tokens,
            messages=messages,
            model=model,
            metadata=metadata,
            stop_sequences=stop_sequences,
            stream=stream,
            system=system,
            temperature=temperature,
            thinking=thinking,
            tool_choice=tool_choice,
            tools=tools,
            top_k=top_k,
            top_p=top_p,
            _is_async=is_async,
            api_key=api_key,
            api_base=api_base,
            client=client,
            custom_llm_provider=custom_llm_provider,
            **kwargs,
        )
        if _should_route_to_responses_api(custom_llm_provider):
            return LiteLLMMessagesToResponsesAPIHandler.anthropic_messages_handler(
                **_shared_kwargs
            )

        # The in-gateway context_management polyfill runs inside
        # ``async_anthropic_messages_handler`` so it can ``await`` the
        # summarization model for ``compact_20260112``. ``context_management``
        # is passed through as a regular kwarg.
        return (
            LiteLLMMessagesToCompletionTransformationHandler.anthropic_messages_handler(
                **_shared_kwargs,
            )
        )

    if custom_llm_provider is None:
        raise ValueError(
            f"custom_llm_provider is required for Anthropic messages, passed in model={model}, custom_llm_provider={custom_llm_provider}"
        )

    local_vars.update(kwargs)
    anthropic_messages_optional_request_params = (
        AnthropicMessagesRequestUtils.get_requested_anthropic_messages_optional_param(
            params=local_vars
        )
    )
    if is_reasoning_auto_summary_enabled():
        thinking_param = anthropic_messages_optional_request_params.get("thinking")
        if (
            isinstance(thinking_param, dict)
            and thinking_param.get("type") != "disabled"
        ):
            anthropic_messages_optional_request_params["thinking"] = {
                **thinking_param,
                "display": "summarized",
            }

    return base_llm_http_handler.anthropic_messages_handler(
        model=model,
        messages=messages,
        anthropic_messages_provider_config=anthropic_messages_provider_config,
        anthropic_messages_optional_request_params=dict(
            anthropic_messages_optional_request_params
        ),
        _is_async=is_async,
        client=client,
        custom_llm_provider=custom_llm_provider,
        litellm_params=litellm_params,
        logging_obj=litellm_logging_obj,
        api_key=api_key,
        api_base=api_base,
        stream=stream,
        kwargs=kwargs,
    )

