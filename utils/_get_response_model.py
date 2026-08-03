from typing import Any, Optional

def _get_response_model(completion_response: Any) -> Optional[str]:
    """
    Extract the model name from a completion response object.

    Used as a fallback for cost calculation when the input model name
    doesn't exist in model_cost (e.g., Azure Model Router).
    """
    if completion_response is None:
        return None

    if isinstance(completion_response, BaseModel):
        return getattr(completion_response, "model", None)
    elif isinstance(completion_response, dict):
        return completion_response.get("model", None)

    return None

