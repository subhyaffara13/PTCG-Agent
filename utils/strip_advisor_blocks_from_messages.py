from typing import Any, List

def strip_advisor_blocks_from_messages(
    messages: List[Any], replace_with_text: bool = False
) -> List[Any]:
    """
    Remove (or replace) server_tool_use (name='advisor') and advisor_tool_result blocks
    from assistant message content.

    Prevents Anthropic 400 invalid_request_error: if advisor_tool_result blocks
    exist in history but the advisor tool is not in the tools array, the API rejects
    the request. This happens when the user has removed the advisor tool for cost
    control or on a follow-up turn.

    Args:
        messages: Conversation history to process (mutated in-place).
        replace_with_text: When True, replace the advisor exchange with an
            <advisor_feedback> text block so the executor retains the semantic
            context of what the advisor said.  When False (default), strip silently.
    """
    for message in messages:
        if not isinstance(message, dict) or message.get("role") != "assistant":
            continue
        content = message.get("content")
        if not isinstance(content, list):
            continue

        # Collect advisor server_tool_use ids and their advice text (for replace mode).
        advisor_id_to_text: dict = {}
        for block in content:
            if (
                isinstance(block, dict)
                and block.get("type") == "server_tool_use"
                and block.get("name") == "advisor"
            ):
                bid = block.get("id")
                if bid:
                    advisor_id_to_text[bid] = None  # text filled in below

        if not advisor_id_to_text:
            continue

        # If replacing, collect the advisor response text from advisor_tool_result blocks.
        if replace_with_text:
            for block in content:
                if (
                    isinstance(block, dict)
                    and block.get("type") == "advisor_tool_result"
                    and block.get("tool_use_id") in advisor_id_to_text
                ):
                    raw = block.get("content") or ""
                    text = (
                        raw
                        if isinstance(raw, str)
                        else next(
                            (
                                b.get("text", "")
                                for b in raw
                                if isinstance(b, dict) and b.get("type") == "text"
                            ),
                            "",
                        )
                    )
                    advisor_id_to_text[block["tool_use_id"]] = text

        new_content = []
        for block in content:
            if not isinstance(block, dict):
                new_content.append(block)
                continue
            is_advisor_use = (
                block.get("type") == "server_tool_use"
                and block.get("name") == "advisor"
                and block.get("id") in advisor_id_to_text
            )
            is_advisor_result = (
                block.get("type") == "advisor_tool_result"
                and block.get("tool_use_id") in advisor_id_to_text
            )
            if is_advisor_use:
                if replace_with_text:
                    advice = advisor_id_to_text.get(block.get("id")) or ""
                    if advice:
                        new_content.append(
                            {
                                "type": "text",
                                "text": f"<advisor_feedback>\n{advice}\n</advisor_feedback>",
                            }
                        )
                # else: drop silently
            elif is_advisor_result:
                pass  # always drop — replaced above (or stripped)
            else:
                new_content.append(block)

        message["content"] = new_content
    return messages

