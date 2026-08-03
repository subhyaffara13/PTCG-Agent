from typing import Any, Dict

def _dump_response(response: Any) -> Dict[str, Any]:
    if isinstance(response, dict):
        return dict(response)
    if hasattr(response, "model_dump"):
        return response.model_dump()
    if hasattr(response, "dict"):
        return response.dict()
    return {"id": _get_response_id(response)}

