from typing import Any, Dict, List, Optional

def _build_responses_kwargs(
    *,
    max_tokens: int,
    messages: List[Dict],
    model: str,
    context_management: Optional[Dict] = None,
    metadata: Optional[Dict] = None,
    output_config: Optional[Dict] = None,
    stop_sequences: Optional[List[str]] = None,
    stream: Optional[bool] = False,
    system: Optional[str] = None,
    temperature: Optional[float] = None,
    thinking: Optional[Dict] = None,
    tool_choice: Optional[Dict] = None,
    tools: Optional[List[Dict]] = None,
    top_k: Optional[int] = None,
    top_p: Optional[float] = None,
    output_format: Optional[Dict] = None,
    extra_kwargs: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """
    Build the kwargs dict to pass directly to litellm.responses() / litellm.aresponses().
    """
    # Build a typed AnthropicMessagesRequest for the adapter
    request_data: Dict[str, Any] = {
        "model": model,
        "messages": messages,
        "max_tokens": max_tokens,
    }
    if context_management:
        request_data["context_management"] = context_management
    if output_config:
        request_data["output_config"] = output_config
    if metadata:
        request_data["metadata"] = metadata
    if system:
        request_data["system"] = system
    if temperature is not None:
        request_data["temperature"] = temperature
    if thinking:
        request_data["thinking"] = thinking
    if tool_choice:
        request_data["tool_choice"] = tool_choice
    if tools:
        request_data["tools"] = tools
    if top_p is not None:
        request_data["top_p"] = top_p
    if output_format:
        request_data["output_format"] = output_format

    anthropic_request = AnthropicMessagesRequest(**request_data)  # type: ignore[typeddict-item]
    responses_kwargs = _ADAPTER.translate_request(anthropic_request)

    # Normalize reasoning effort based on model capabilities
    # (e.g. "max" → "xhigh"/"high", "minimal" → "low" if unsupported)
    reasoning = responses_kwargs.get("reasoning")
    if isinstance(reasoning, dict) and "effort" in reasoning:
        from litellm.llms.anthropic.experimental_pass_through.utils import (
            normalize_reasoning_effort_value,
        )

        effort = reasoning["effort"]
        normalized = normalize_reasoning_effort_value(
            effort,
            model=model,
            custom_llm_provider=(extra_kwargs or {}).get("custom_llm_provider"),
        )
        if normalized != effort:
            responses_kwargs["reasoning"] = {**reasoning, "effort": normalized}

    if stream:
        responses_kwargs["stream"] = True

    # Forward litellm-specific kwargs (api_key, api_base, logging obj, etc.)
    excluded = {"anthropic_messages"}
    for key, value in (extra_kwargs or {}).items():
        if key == "litellm_logging_obj" and value is not None:
            from litellm.litellm_core_utils.litellm_logging import (
                Logging as LiteLLMLoggingObject,
            )
            from litellm.types.utils import CallTypes

            if isinstance(value, LiteLLMLoggingObject):
                # Keep call_type as anthropic_messages so spend_logs are billed
                # against /v1/messages; the success handler translates the
                # Responses API result back to a ModelResponse for the row.
                setattr(value, "call_type", CallTypes.anthropic_messages.value)
            responses_kwargs[key] = value
        elif key not in excluded and key not in responses_kwargs and value is not None:
            responses_kwargs[key] = value

    return responses_kwargs

