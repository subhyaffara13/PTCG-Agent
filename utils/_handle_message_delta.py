from typing import Dict

def _handle_message_delta(data: Dict, response: Dict) -> None:
    delta = data.get("delta", {})
    if "stop_reason" in delta:
        response["stop_reason"] = delta["stop_reason"]
    if "stop_sequence" in delta:
        response["stop_sequence"] = delta["stop_sequence"]
    usage = data.get("usage", {})
    if usage.get("output_tokens") is not None:
        response["usage"]["output_tokens"] = usage["output_tokens"]
    for key in (
        "input_tokens",
        "cache_creation_input_tokens",
        "cache_read_input_tokens",
    ):
        if key in usage:
            response["usage"][key] = usage[key]

