
def _maybe_normalize_passthrough(
    span: "Span",
    kwargs: dict,
    raw_response_obj,
    coerced_response_obj,
    standard_logging_payload,
) -> None:
    """Surface input/output text for passthrough routes (e.g. Bedrock
    InvokeModel) so the parent span renders as more than `usage` numbers.

    Only runs when `call_type` is a passthrough variant. Reads from:
      - `kwargs["additional_args"]["complete_input_dict"]` for input
      - the coerced response (or `kwargs["original_response"]`) for output

    All emits are best-effort: if the provider shape isn't recognized the
    helper exits silently. Existing chat/completion paths never enter this
    helper because their call_type doesn't contain "passthrough".

    TEMPORARY BRIDGE: passthrough handlers don't populate the
    StandardLoggingPayload `messages` field today (they call
    `transform_response(messages=[])`), so the input is only available via
    `additional_args.complete_input_dict`. The proper fix is upstream in
    `base_passthrough_logging_handler._create_response_logging_payload()`:
    once that populates SLP `messages`/`response`, every callback gets
    passthrough I/O (with central redaction) for free and this helper's
    `complete_input_dict` fallback can be deleted. See follow-up issue.
    """
    call_type = (
        standard_logging_payload.get("call_type")
        if isinstance(standard_logging_payload, dict)
        else None
    )
    if not _is_passthrough_call_type(call_type):
        return

    # Respect LiteLLM's central message-redaction contract. The normal
    # chat/completion path is redacted by `perform_redaction` before
    # callbacks run, but `complete_input_dict` (read below) is NOT covered by
    # that layer — so without this gate, an operator who enabled redaction
    # would still see raw passthrough prompts in Arize. Skip entirely when
    # redaction is on so neither input nor output leaks through this bridge.
    if should_redact_message_logging(kwargs):
        return

    # --- INPUT --------------------------------------------------------------
    additional_args = kwargs.get("additional_args") or {}
    complete_input_dict = (
        additional_args.get("complete_input_dict")
        if isinstance(additional_args, dict)
        else None
    )
    if isinstance(complete_input_dict, dict):
        _set_passthrough_input_attributes(span, complete_input_dict.get("messages"))

    # --- OUTPUT -------------------------------------------------------------
    parsed_response = _parse_passthrough_response(
        raw_response_obj, coerced_response_obj, kwargs
    )
    if not isinstance(parsed_response, dict):
        return

    _set_passthrough_output_attributes(span, parsed_response)

