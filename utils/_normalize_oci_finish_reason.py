from typing import Optional

def _normalize_oci_finish_reason(raw: Optional[str]) -> Optional[str]:
    """Map an OCI-specific finish reason to its OpenAI-standard equivalent.

    OCI emits ``COMPLETE`` / ``MAX_TOKENS`` / ``TOOL_CALL(S)`` plus a long tail
    of error/cancel reasons (``ERROR``, ``ERROR_TOXIC``, ``ERROR_LIMIT``,
    ``USER_CANCEL``, ``CONTENT_FILTERED``, ``CANCELLED``, ...). The OpenAI
    spec only defines ``stop`` / ``length`` / ``tool_calls`` / ... — anything
    else is collapsed to ``"stop"`` so downstream consumers switching on
    ``finish_reason`` keep working. A ``None`` input passes through unchanged.
    """
    if raw is None:
        return None
    if raw == "COMPLETE":
        return "stop"
    if raw == "MAX_TOKENS":
        return "length"
    if raw in ("TOOL_CALL", "TOOL_CALLS"):
        return "tool_calls"
    return "stop"

