from typing import Any, Optional

def _get_response_id(response: Any) -> Optional[str]:
    if response is None:
        return None
    if isinstance(response, dict):
        value = response.get("id")
    else:
        value = getattr(response, "id", None)
    return value if isinstance(value, str) else None

