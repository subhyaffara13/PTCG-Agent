
def truncate_message(message: dict, max_tokens: int) -> dict:
    """
    Truncate a message's content to approximately max_tokens by keeping
    the first 70% and last 30% of lines with a separator in between.

    Uses line-based splitting to preserve code structure (function
    boundaries, indentation) rather than word-based splitting which
    mangles code.

    Used when a message is too large to fit entirely in the budget but
    too relevant to fully stub out.
    """
    content = message.get("content", "")
    if isinstance(content, list):
        content = " ".join(
            p.get("text", "") if isinstance(p, dict) else str(p) for p in content
        )

    # Rough conversion: 1 token ≈ 3 characters
    target_chars = max(100, max_tokens * 3)

    if len(content) <= target_chars:
        return {**message, "content": content}

    lines = content.split("\n")

    # Estimate target line count from character budget
    avg_line_len = max(1, len(content) // max(1, len(lines)))
    target_lines = max(2, target_chars // avg_line_len)

    if len(lines) <= target_lines:
        return {**message, "content": content}

    first_count = (target_lines * 7) // 10
    last_count = target_lines - first_count
    truncated = (
        "\n".join(lines[:first_count])
        + "\n...[truncated for context window]...\n"
        + "\n".join(lines[-last_count:])
    )
    return {**message, "content": truncated}

