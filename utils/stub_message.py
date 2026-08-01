
def stub_message(message: dict, key: str) -> dict:
    """
    Replace message content with a compact stub.

    Returns a new message dict with the same role but content replaced
    with a short description referencing the retrieval tool.
    """
    content = message.get("content", "")
    if isinstance(content, list):
        content = " ".join(
            p.get("text", "") if isinstance(p, dict) else str(p) for p in content
        )

    line_count = content.count("\n") + 1
    content_type = detect_content_type(content)

    stub_content = (
        f"[Compressed: {key} — {line_count} lines, {content_type}. "
        f"Use litellm_content_retrieve tool to get full content.]"
    )

    return {**message, "content": stub_content}

