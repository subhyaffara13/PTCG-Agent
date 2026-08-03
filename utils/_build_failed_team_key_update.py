from typing import Any, Dict, Optional

def _build_failed_team_key_update(
    token: str,
    exception: Exception,
    existing_key_row: Optional[LiteLLM_VerificationToken],
) -> FailedKeyUpdate:
    """Normalize an exception from the per-key update loop into a FailedKeyUpdate."""
    if isinstance(exception, HTTPException):
        detail = exception.detail
        if isinstance(detail, dict):
            error_message = detail.get("error", str(exception))
        else:
            error_message = str(detail)
    elif isinstance(exception, ProxyException):
        error_message = exception.message
    else:
        error_message = str(exception)

    key_info: Optional[Dict[str, Any]] = None
    if existing_key_row is not None:
        if hasattr(existing_key_row, "model_dump"):
            key_info = existing_key_row.model_dump()
        elif hasattr(existing_key_row, "dict"):
            key_info = existing_key_row.dict()
        if key_info:
            key_info.pop("token", None)

    return FailedKeyUpdate(key=token, key_info=key_info, failed_reason=error_message)

