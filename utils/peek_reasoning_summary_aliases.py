
def peek_reasoning_summary_aliases(optional_params: dict) -> Optional[Any]:
    """Read AI-SDK-style reasoning summary from optional_params or nested extra_body.

    Uses key membership (not ``or`` chains) so falsy values like ``""`` are not skipped.
    """
    if "reasoningSummary" in optional_params:
        return optional_params["reasoningSummary"]
    if "reasoning_summary" in optional_params:
        return optional_params["reasoning_summary"]
    extra_body = optional_params.get("extra_body")
    if isinstance(extra_body, dict):
        if "reasoningSummary" in extra_body:
            return extra_body["reasoningSummary"]
        if "reasoning_summary" in extra_body:
            return extra_body["reasoning_summary"]
    return None

