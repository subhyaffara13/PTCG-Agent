from typing import Any, List

def _sanitize_empty_text_content(
    message: AllMessageValues,
) -> AllMessageValues:
    """
    Case C: Sanitize empty text content
    - Replace empty or whitespace-only text content with a placeholder message.
    - Handles both string content and list-of-blocks content (rewriting only
      the empty text blocks in place; non-text blocks like images are left
      untouched).

    Returns:
        The message with sanitized content if needed, otherwise the original message
    """
    if message.get("role") not in ["user", "assistant"]:
        return message

    content = message.get("content")

    if isinstance(content, str):
        if not content or not content.strip():
            message = cast(AllMessageValues, dict(message))  # Make a copy
            message["content"] = _EMPTY_TEXT_PLACEHOLDER
            verbose_logger.debug(
                f"_sanitize_empty_text_content: Replaced empty text content in {message.get('role')} message"
            )
        return message

    if isinstance(content, list):
        # Walk the blocks and rewrite any empty text blocks. We rewrite (rather
        # than drop) so callers don't end up with an entirely empty content
        # list, which Anthropic also rejects.
        new_blocks: List[Any] = []
        rewrote_any = False
        for block in content:
            if isinstance(block, dict) and block.get("type") == "text":
                text = block.get("text")
                if not isinstance(text, str) or not text or not text.strip():
                    new_block = dict(block)
                    new_block["text"] = _EMPTY_TEXT_PLACEHOLDER
                    new_blocks.append(new_block)
                    rewrote_any = True
                    continue
            new_blocks.append(block)

        if rewrote_any:
            message = cast(AllMessageValues, dict(message))  # Make a copy
            message["content"] = new_blocks  # type: ignore
            verbose_logger.debug(
                f"_sanitize_empty_text_content: Replaced empty text block(s) in {message.get('role')} message"
            )

    return message

