
def _build_litellm_metadata_for_ws(kwargs: dict) -> dict:
    metadata: dict = {**(kwargs.get("litellm_metadata") or {})}
    guardrails = (
        (kwargs.get("metadata") or {}).get("guardrails")
        or kwargs.get("guardrails")
        or []
    )
    if guardrails:
        metadata["guardrails"] = guardrails
    return metadata

