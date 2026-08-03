from typing import Any

def _build_generate_return(record: dict[str, Any]) -> dict[str, Any]:
    """Build a legacy ``GenerateReturn``-shaped dict from a call record.

    Omits raw prompts and responses to avoid duplicating large content
    already available via ``call_details`` and ``thoughts``.
    """
    gr: dict[str, Any] = {
        "request_for_logging": {
            "model": record["model"],
        },
        "response_for_logging": {
            "finish_reason": record.get("finish_reason"),
        },
        "generation_tokens": record.get("generation_tokens"),
        "prompt_tokens": record.get("prompt_tokens"),
        "total_tokens": record.get("total_tokens"),
        "duration_success_only_secs": record.get("duration_secs"),
    }
    reasoning = record.get("reasoning_tokens")
    if reasoning is not None:
        gr["reasoning_tokens"] = reasoning
    return gr

