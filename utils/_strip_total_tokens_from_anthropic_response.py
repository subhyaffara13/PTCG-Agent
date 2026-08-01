
def _strip_total_tokens_from_anthropic_response(response: Any) -> None:
    """Remove the OpenAI-flavored `usage.total_tokens` field that LiteLLM
    injects into Anthropic /v1/messages responses.

    The Anthropic /v1/messages spec only defines:
        input_tokens, output_tokens, cache_creation_input_tokens,
        cache_read_input_tokens, cache_creation.{ephemeral_5m,ephemeral_1h}
    The streaming SSE path (message_delta.usage) already does not include
    total_tokens; this brings the non-streaming path into the same shape.

    Handles both shapes returned by `base_process_llm_request`:
    - plain `dict` (most common — `AnthropicMessagesResponse` is a TypedDict
      and is `dict` at runtime)
    - Pydantic model whose `usage` attribute is dict-shaped (e.g. a
      BaseModel that holds raw Anthropic usage as a `dict[str, int]`)

    Streaming results (StreamingResponse, AsyncIterator, etc.) and Pydantic
    models with strongly-typed Usage sub-models are left untouched —
    those paths either have separate serialization handling or impose
    type constraints the helper does not try to subvert.
    """
    if response is None:
        return
    if isinstance(response, dict):
        usage = response.get("usage")
        if isinstance(usage, dict) and "total_tokens" in usage:
            usage.pop("total_tokens", None)
        return
    # Pydantic-model fallback: only mutate if `usage` is a dict.
    usage = getattr(response, "usage", None)
    if isinstance(usage, dict) and "total_tokens" in usage:
        usage.pop("total_tokens", None)

