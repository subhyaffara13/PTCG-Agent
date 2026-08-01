
def apply_redacted_messages_back(
    data: Dict[str, Any], redacted_messages: List[Dict[str, Any]]
) -> None:
    """Write redacted messages back to whichever field(s) the caller used.

    Mask/anonymize paths take a synthesised messages list (from
    :func:`build_inspection_messages`), get a redacted version back from a
    third-party guardrail, and need to rewrite the request body. Writing
    only to ``data["messages"]`` leaves the Responses-API ``data["input"]``
    field untouched, so the unredacted text still reaches the LLM.

    This helper updates both fields when both are present.
    """
    if "messages" in data:
        data["messages"] = redacted_messages
    if isinstance(data.get("input"), str):
        text_parts: List[str] = []
        for msg in redacted_messages:
            if not isinstance(msg, dict):
                continue
            text_parts.extend(_iter_text_parts_in_content(msg.get("content")))
        data["input"] = "\n".join(text_parts)

