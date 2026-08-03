from typing import Dict

def _handle_message_start(data: Dict, response: Dict) -> None:
    msg = data.get("message", {})
    response["id"] = msg.get("id", response["id"])
    response["model"] = msg.get("model", response["model"])
    response["role"] = msg.get("role", response["role"])
    usage = msg.get("usage", {})
    if usage:
        response["usage"]["input_tokens"] = usage.get("input_tokens", 0)
        for key in ("cache_creation_input_tokens", "cache_read_input_tokens"):
            if key in usage:
                response["usage"][key] = usage[key]

