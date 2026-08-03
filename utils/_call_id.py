from typing import Any

def _call_id(
    payload: "StandardLoggingPayload | None", kwargs: Mapping[str, Any]
) -> str | None:
    """The call id from the payload (when closed) or the bare kwargs (at pre_call)."""
    if payload is not None:
        call_id = as_str(payload.get("litellm_call_id")) or as_str(payload.get("id"))
        if call_id:
            return call_id
    return as_str(kwargs.get("litellm_call_id"))

