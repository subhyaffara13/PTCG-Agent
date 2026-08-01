
def get_request_guardrails(kwargs: Dict[str, Any]) -> List[str]:
    """
    Get the request guardrails from the kwargs
    """
    metadata = kwargs.get("metadata") or {}
    requester_metadata = metadata.get("requester_metadata") or {}
    applied_guardrails = requester_metadata.get("guardrails") or []
    return applied_guardrails

