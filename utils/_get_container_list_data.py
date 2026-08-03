from typing import Any, List, Optional

def _get_container_list_data(response: Any) -> Optional[List[Any]]:
    if response is None:
        return None
    if isinstance(response, dict):
        data = response.get("data")
    else:
        data = getattr(response, "data", None)
    return data if isinstance(data, list) else None

