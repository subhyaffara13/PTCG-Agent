
def parse_reasoning(processor, generated_ids, content: str, reasoning_config: dict) -> tuple[str, str | None]:
    """Split generated output into ``(content, reasoning_content)`` via ``parse_response``.

    If the schema's regex matches (closing marker present), use it. For prompts
    that prefill the opener (QwQ-32B, DeepSeek-R1) the entire output is reasoning
    until ``</think>`` arrives — when that's truncated, fall back to treating
    all decoded text as reasoning. Returns ``(content, None)`` otherwise.
    """
    parsed = processor.parse_response(generated_ids, reasoning_config["schema"])
    if parsed:
        reasoning = parsed.get("thinking", "")
        if reasoning:
            return parsed.get("content", ""), reasoning
    # Prefilled opener (QwQ-32B, DeepSeek-R1) truncated before ``</think>`` —
    # no anchor for the schema regex; treat all output as reasoning.
    if reasoning_config.get("start_in_thinking"):
        return "", content
    return content, None

