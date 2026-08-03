from typing import Any, Dict

def _empty_list_response() -> Dict[str, Any]:
    return {
        "object": "list",
        "data": [],
        "first_id": None,
        "last_id": None,
        "has_more": False,
    }

