from typing import Any, Dict, List, Optional

def _detect_exhaustion(
    status: Optional[int], tool_results: List[Dict[str, Any]]
) -> bool:
    if status is not None and status in _EXHAUSTION_STATUSES:
        return True
    for r in tool_results:
        content = str(r.get("content", "")).lower()
        if any(kw in content for kw in _EXHAUSTION_KEYWORDS):
            return True
    return False

