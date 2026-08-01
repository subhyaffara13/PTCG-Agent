
def _collect_stream_delta_text_holders(delta: Any) -> List[_DeltaHolder]:
    """
    Collect the user-visible text strings a Bedrock Converse ``contentBlockDelta``
    can carry, matching the coverage of the non-streaming output handler.

    Each holder is ``(group_key, container, key)`` where ``container[key]`` is the
    text. ``group_key`` ties together fragments that belong to the same logical
    stream (e.g. a single mask token split across frames) so they are
    concatenated before guardrailing and redistributed afterwards. Structural
    values such as reasoning signatures, redacted reasoning and citation sources
    are left out so they are never rewritten.
    """
    holders: List[_DeltaHolder] = []
    if not isinstance(delta, dict):
        return holders
    if isinstance(delta.get("text"), str):
        holders.append(("text", delta, "text"))
    tool_use = delta.get("toolUse")
    if isinstance(tool_use, dict) and isinstance(tool_use.get("input"), str):
        holders.append(("tool", tool_use, "input"))
    reasoning = delta.get("reasoningContent")
    if isinstance(reasoning, dict) and isinstance(reasoning.get("text"), str):
        holders.append(("reasoning", reasoning, "text"))
    citations = delta.get("citationsContent")
    if isinstance(citations, dict):
        for index, cited in enumerate(citations.get("content") or []):
            if isinstance(cited, dict) and isinstance(cited.get("text"), str):
                holders.append((("citation", index), cited, "text"))
    return holders

