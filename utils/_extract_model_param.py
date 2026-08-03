from typing import Optional

def _extract_model_param(request: "Request", request_body: dict) -> Optional[str]:
    """
    Extract model parameter from request.

    Priority:
    1. request_body.model
    2. Query parameter (?model=)
    3. Header (x-litellm-model)
    """
    return (
        request_body.get("model")
        or request.query_params.get("model")
        or request.headers.get("x-litellm-model")
    )

