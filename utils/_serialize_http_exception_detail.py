import json
from typing import Any, Optional, Tuple

def _serialize_http_exception_detail(
    detail: Any,
) -> Tuple[str, Optional[dict]]:
    """
    Convert an HTTPException.detail value into (message, structured_fields)
    for ProxyException / SSE error frames.

    Dict-detail HTTPExceptions raised by guardrails were previously str()-mangled
    into a Python repr blob, producing unparseable error responses on both the
    streaming and non-streaming proxy surfaces. This helper extracts a clean
    human-readable message while preserving the full payload as structured
    fields, so the dominant guardrail shapes (`{"error": "..."}` flat and
    `{"error": {"message": "..."}}` nested) both round-trip cleanly.
    """
    if isinstance(detail, str):
        return detail, None
    if isinstance(detail, dict):
        err = detail.get("error")
        if isinstance(err, str):
            return err, detail
        if isinstance(err, dict):
            nested_msg = err.get("message")
            if isinstance(nested_msg, str):
                return nested_msg, detail
        msg = detail.get("message")
        if isinstance(msg, str):
            return msg, detail
        return json.dumps(detail), detail
    return str(detail), None

