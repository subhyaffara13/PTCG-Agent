
def _carry_guardrail_logging_info(
    request_data: dict, guardrail_data: Optional[dict]
) -> None:
    """Copy guardrail logging entries from ``guardrail_data`` onto ``request_data``.

    Post-call guardrails run against a throwaway ``hook_data`` dict (its
    ``metadata`` is what ``_init_kwargs_for_pass_through_endpoint`` already
    stripped off ``_parsed_body``), so a block records the
    ``standard_logging_guardrail_information`` there and not on the dict the
    failure handler forwards to ``post_call_failure_hook``. Without this the
    otel guardrail span is emitted on allow but missing on block. Carry the
    entries over so the failure path matches the unified path.
    """
    if guardrail_data is None:
        return
    source_metadata = guardrail_data.get("metadata")
    if not isinstance(source_metadata, dict):
        return
    entries = source_metadata.get("standard_logging_guardrail_information")
    if not entries:
        return

    metadata = request_data.get("metadata")
    if not isinstance(metadata, dict):
        metadata = request_data["metadata"] = {}
    metadata.setdefault("standard_logging_guardrail_information", list(entries))

