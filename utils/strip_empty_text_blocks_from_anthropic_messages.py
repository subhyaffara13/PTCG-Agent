
def strip_empty_text_blocks_from_anthropic_messages(
    messages: List[Any],
) -> List[Any]:
    """
    Return a new message list with empty or whitespace-only ``{"type": "text"}``
    content blocks removed.

    Anthropic's API rejects requests containing such blocks with
    ``"messages: text content blocks must be non-empty"``, but assistant
    messages from Anthropic routinely arrive with ``{"type": "text", "text": ""}``
    alongside ``tool_use`` blocks (see anthropics/anthropic-sdk-python#461).
    Multi-turn tool-use clients (e.g. Claude Code) loop these prior responses
    back as conversation history, which then causes the next request to 400
    on the unified ``/v1/messages`` path.  ``/v1/chat/completions`` already
    handles this in ``anthropic_messages_pt``; this helper provides the
    equivalent guarantee for the native Anthropic Messages path.

    Messages whose content is a list and becomes empty after stripping are
    omitted, matching :func:`strip_thinking_blocks_from_anthropic_messages`.
    The caller's list and its content blocks are never mutated; modified
    messages are returned as shallow copies with a fresh content list.
    """
    out: List[Any] = []
    for m in messages:
        if not isinstance(m, dict) or not isinstance(m.get("content"), list):
            out.append(m)
            continue
        content = m["content"]
        filtered = [b for b in content if not _is_empty_text_block(b)]
        if len(filtered) == len(content):
            out.append(m)
        elif filtered:
            out.append({**m, "content": filtered})
    return out

