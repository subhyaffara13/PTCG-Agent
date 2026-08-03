from typing import Optional

def _sanitize_optional_params(optional_params: Optional[dict]) -> dict:
    if not isinstance(optional_params, dict):
        return {}
    optional_params.pop("secret_fields", None)
    return optional_params

