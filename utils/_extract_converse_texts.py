
def _extract_converse_texts(
    body: dict,
    skip_system: bool,
    skip_tool: bool,
) -> Tuple[List[str], List[_StringHolder]]:
    """
    Walk a Bedrock Converse request body and collect text content.

    Returns (texts, holders) where each holder is the (container, key) pair
    that owns the extracted string, so write-back mutates it in place. Besides
    top-level ``text`` blocks this scans the arbitrary-JSON fields a caller can
    hide prompt content in -- ``toolUse.input`` and
    ``toolResult.content[].json`` (alongside ``toolResult.content[].text``) --
    as well as the request-level fields still forwarded to Bedrock that a caller
    can route blocked content through: ``toolConfig.tools`` (tool names,
    descriptions and input schemas) and ``additionalModelRequestFields``. Tool
    message blocks are skipped when tool messages are excluded, but tool
    definitions are always scanned to match the chat-completions guardrail path.
    """
    holders: List[_StringHolder] = []

    if not skip_system:
        for block in body.get("system") or []:
            if isinstance(block, dict):
                _collect_block_text(block, holders)

    for message in body.get("messages") or []:
        if not isinstance(message, dict):
            continue
        for block in message.get("content") or []:
            if not isinstance(block, dict):
                continue
            if skip_tool and ("toolUse" in block or "toolResult" in block):
                continue
            _collect_block_text(block, holders)
            tool_use = block.get("toolUse")
            if isinstance(tool_use, dict):
                _collect_strings(tool_use.get("input"), holders)
            tool_result = block.get("toolResult")
            if isinstance(tool_result, dict):
                for inner in tool_result.get("content") or []:
                    if isinstance(inner, dict):
                        _collect_block_text(inner, holders)
                        _collect_strings(inner.get("json"), holders)

    tool_config = body.get("toolConfig")
    if isinstance(tool_config, dict):
        _collect_strings(tool_config.get("tools"), holders)

    _collect_strings(body.get("additionalModelRequestFields"), holders)

    texts = [container[key] for container, key in holders]
    return texts, holders

