from typing import Optional

def _is_passthrough_call_type(call_type: Optional[str]) -> bool:
    if not call_type:
        return False
    lowered = str(call_type).lower()
    return "passthrough" in lowered or "pass_through" in lowered

