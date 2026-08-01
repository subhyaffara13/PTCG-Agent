
def _fast_serialize_simple_model_response_stream(
    chunk: ModelResponseStream,
) -> Optional[bytes]:
    """
    Serialize the common OpenAI text streaming chunk without the full Pydantic
    serializer. Fall back for richer chunks so tool calls, logprobs, usage, and
    provider-specific fields keep the canonical model_dump_json behavior.
    """
    if (
        getattr(chunk, "provider_specific_fields", None) is not None
        or getattr(chunk, "system_fingerprint", None) is not None
        or getattr(chunk, "usage", None) is not None
    ):
        return None

    choices = getattr(chunk, "choices", None)
    if not isinstance(choices, list) or len(choices) != 1:
        return None

    choice = choices[0]
    if (
        getattr(choice, "logprobs", None) is not None
        or getattr(choice, "enhancements", None) is not None
    ):
        return None

    delta = getattr(choice, "delta", None)
    if delta is None:
        return None

    unsupported_delta_fields = (
        "function_call",
        "tool_calls",
        "audio",
        "images",
        "annotations",
        "reasoning_content",
        "thinking_blocks",
        "provider_specific_fields",
        "refusal",
    )
    if any(
        getattr(delta, field, None) is not None for field in unsupported_delta_fields
    ):
        return None

    delta_dict: dict = {}
    role = getattr(delta, "role", None)
    content = getattr(delta, "content", None)
    if role is not None:
        delta_dict["role"] = role
    if content is not None:
        delta_dict["content"] = content

    choice_dict = {"index": getattr(choice, "index", 0), "delta": delta_dict}
    finish_reason = getattr(choice, "finish_reason", None)
    if finish_reason is not None:
        choice_dict["finish_reason"] = finish_reason

    # Match the canonical ``model_dump_json(exclude_none=True)`` shape — if a
    # field is None, omit it entirely rather than emitting ``"key": null``.
    # Strict OpenAI-compatible clients reject ``null`` for optional fields like
    # ``model``, so diverging here would surface as a client-side regression
    # only on the fast path. Fall back to the slow path if a required-looking
    # top-level identifier is missing.
    model = getattr(chunk, "model", None)
    if model is None:
        return None

    payload: dict = {
        "id": getattr(chunk, "id", None),
        "object": getattr(chunk, "object", None),
        "created": getattr(chunk, "created", None),
        "model": model,
        "choices": [choice_dict],
    }
    for top_level_key in ("id", "object", "created"):
        if payload[top_level_key] is None:
            payload.pop(top_level_key)
    return orjson.dumps(payload)

