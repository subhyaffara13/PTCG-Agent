import json
from typing import Any, Dict, List

def _parse_guardrail_info_from_payload(payload: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Extract guardrail_information from spend log payload metadata."""
    meta = payload.get("metadata")
    if not meta:
        return []
    if isinstance(meta, str):
        try:
            meta = json.loads(meta)
        except (json.JSONDecodeError, TypeError):
            return []
    if not isinstance(meta, dict):
        return []
    info = meta.get("guardrail_information") or meta.get(
        "standard_logging_guardrail_information"
    )
    if not isinstance(info, list):
        return []
    return info

