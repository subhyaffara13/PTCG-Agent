from typing import Optional

def _count_content_list(
    count_function: TokenCounterFunction,
    content_list: OpenAIMessageContent,
    use_default_image_token_count: bool,
    default_token_count: Optional[int],
) -> int:
    """
    Recursively count tokens from a list of content blocks.
    """
    try:
        num_tokens = 0
        for c in content_list:
            if isinstance(c, str):
                num_tokens += count_function(c)
            elif c["type"] == "text":
                num_tokens += count_function(str(c.get("text", "")))
            elif c["type"] == "image_url":
                image_url = c.get("image_url")
                num_tokens += _count_image_tokens(
                    image_url, use_default_image_token_count
                )
            elif c["type"] in ("tool_use", "tool_result"):
                num_tokens += _count_anthropic_content(
                    c,
                    count_function,
                    use_default_image_token_count,
                    default_token_count,
                )
            elif c["type"] == "thinking":
                # Claude extended thinking content block
                # Count the thinking text and skip signature (opaque signature blob)
                thinking_text = str(c.get("thinking", ""))
                if thinking_text:
                    num_tokens += count_function(thinking_text)
            elif c["type"] == "tool_reference":
                # Anthropic tool-search reference block: a lightweight pointer to
                # a deferred tool, e.g. {"type": "tool_reference", "tool_name": ...}.
                # The full tool definition is counted via the `tools` param, so we
                # only count the referenced name here. Without this branch,
                # token_counter raises on tool-search traffic; on the streaming
                # anthropic_messages path that nulls response_cost and causes the
                # proxy to drop the SpendLogs row entirely (silent cost undercount).
                tool_name = str(c.get("tool_name") or "")
                if tool_name:
                    num_tokens += count_function(tool_name)
            else:
                content_type = (
                    c.get("type", type(c).__name__)
                    if isinstance(c, dict)
                    else type(c).__name__
                )
                raise ValueError(
                    f"Invalid content item type: {content_type}. "
                    f"Expected str or dict with 'type' field (text, image_url, tool_use, tool_result, thinking, tool_reference)."
                )
        return num_tokens
    except Exception as e:
        if default_token_count is not None:
            return default_token_count
        raise ValueError(
            f"Error getting number of tokens from content list: {e}, "
            f"default_token_count={default_token_count}"
        )

