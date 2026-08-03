from typing import Dict, Optional

def add_guardrail_to_applied_guardrails_header(
    request_data: Dict, guardrail_name: Optional[str]
):
    if guardrail_name is None:
        return
    _, _metadata = _get_or_create_proxy_metadata_bucket(request_data)
    if "applied_guardrails" in _metadata:
        if guardrail_name not in _metadata["applied_guardrails"]:
            _metadata["applied_guardrails"].append(guardrail_name)
    else:
        _metadata["applied_guardrails"] = [guardrail_name]

