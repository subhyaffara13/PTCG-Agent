
def _build_litellm_metadata(kwargs: dict) -> dict:
    """Build the litellm_metadata dict for guardrail checking (internal only, not forwarded to provider)."""
    metadata: dict = {**(kwargs.get("litellm_metadata") or {})}
    guardrails = (
        (kwargs.get("metadata") or {}).get("guardrails")
        or kwargs.get("guardrails")
        or []
    )
    if guardrails:
        metadata["guardrails"] = guardrails
    return metadata

