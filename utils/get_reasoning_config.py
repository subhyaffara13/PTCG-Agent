
def get_reasoning_config(processor, model: "PreTrainedModel", input_ids=None) -> dict | None:
    """Return reasoning config for the model, or ``None`` if not supported.

    The config drives both streaming detection (token IDs) and post-hoc parsing
    (response schema). Returns a dict with:
        - ``start_ids`` (`list[int]`): Token ID sequence that opens a thinking block.
        - ``end_id`` (`int`): Token ID that closes the block.
        - ``schema`` (`dict`): Response schema with ``thinking`` / ``content``
          properties for :func:`parse_reasoning`.
        - ``start_in_thinking`` (`bool`, only when ``input_ids`` is given): Whether
          the rendered prompt already opened an unclosed thinking block (prefilled
          by the template), so the model's output begins inside the block.
    """
    tokenizer = getattr(processor, "tokenizer", processor)
    model_type = model.config.model_type.lower()
    thinking_tokens = next(
        (v for k, v in _THINKING_TOKENS.items() if k == model_type),
        _DEFAULT_THINKING_TOKENS,
    )
    start_ids = [tokenizer.convert_tokens_to_ids(t) for t in thinking_tokens["start"]]
    end_id = tokenizer.convert_tokens_to_ids(thinking_tokens["end"])
    if any(tid in (None, tokenizer.unk_token_id) for tid in start_ids) or end_id in (None, tokenizer.unk_token_id):
        return None
    # Custom-token families (e.g. Gemma 4) provide their schema via the tokenizer;
    # default ``<think>`` falls back to the schema baked into ``_DEFAULT_THINKING_TOKENS``.
    schema = getattr(tokenizer, "response_schema", None)
    if not (schema and "thinking" in schema["properties"]):
        schema = _DEFAULT_THINKING_TOKENS["schema"]
    config: dict = {"start_ids": start_ids, "end_id": end_id, "schema": schema}
    if input_ids is not None:
        config["start_in_thinking"] = _starts_in_thinking(input_ids, start_ids)
    return config

