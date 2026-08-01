
def _build_call_detail(
    record: dict[str, Any],
    save_prompt: bool,
    save_response: bool,
) -> dict[str, Any]:
    """Build a single ``call_details`` entry from an internal call record."""
    detail: dict[str, Any] = {
        "model": record["model"],
        "prompt_tokens": record["prompt_tokens"],
        "generation_tokens": record["generation_tokens"],
        "total_tokens": record["total_tokens"],
        "finish_reason": record["finish_reason"],
        "duration_secs": record["duration_secs"],
    }
    if save_response:
        detail["response"] = record["content"]
    if "reasoning_tokens" in record:
        detail["reasoning_tokens"] = record["reasoning_tokens"]
    if "first_token_secs" in record:
        detail["first_token_secs"] = record["first_token_secs"]
    if save_prompt:
        detail["prompt"] = record["prompt"]
    return detail

