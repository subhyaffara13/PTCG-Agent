
def get_tool_call_config(processor, model: "PreTrainedModel") -> dict | None:
    """Return tool call config for the model, or ``None`` if tool calls are not supported.

    Returns a dict with:
        - ``schema`` (`dict`): Schema to pass to ``tokenizer.parse_response(block, schema)``.
        - ``stc_id`` (`int`): Token ID of the start-of-tool-call delimiter.
        - ``etc_id`` (`int`): Token ID of the end-of-tool-call delimiter.
    """
    tokenizer = getattr(processor, "tokenizer", processor)
    stc = getattr(tokenizer, "stc_token", None)
    etc = getattr(tokenizer, "etc_token", None)
    response_schema = getattr(tokenizer, "response_schema", None)

    # Models with full tokenizer config (e.g. Gemma 4)
    if stc and etc and response_schema:
        schema = response_schema["properties"]["tool_calls"]
    else:
        # Fallback: known model families without full tokenizer config. Matched by exact
        # model_type against the tuple keys of _TOOL_CALL_FALLBACKS.
        model_type = model.config.model_type
        fallback = next((v for types, v in _TOOL_CALL_FALLBACKS.items() if model_type in types), None)
        if fallback is None:
            return None
        stc, etc, schema = fallback["stc"], fallback["etc"], fallback["schema"]

    stc_id = tokenizer.convert_tokens_to_ids(stc)
    etc_id = tokenizer.convert_tokens_to_ids(etc)
    return {"schema": schema, "stc_id": stc_id, "etc_id": etc_id}

