import json
from typing import Union

def _extract_error_from_sse_chunk(event_line: Union[str, bytes]) -> dict:
    """
    Extract error dictionary from SSE format chunk.

    Args:
        event_line: SSE format event line, e.g. "data: {"error": {...}}\n\n"

    Returns:
        Error dictionary in OpenAI API format
    """
    event_line = (
        event_line.decode("utf-8") if isinstance(event_line, bytes) else event_line
    )

    # Default error format
    default_error = {
        "message": "Unknown error",
        "type": "internal_server_error",
        "param": None,
        "code": "500",
    }

    if event_line.startswith("data: "):
        json_str = event_line[len("data: ") :].strip()
        if not json_str or json_str == "[DONE]":
            return default_error

        try:
            data = orjson.loads(json_str)
            if isinstance(data, dict) and "error" in data:
                error_obj = data["error"]
                if isinstance(error_obj, dict):
                    return error_obj
        except (orjson.JSONDecodeError, json.JSONDecodeError):
            pass

    return default_error

