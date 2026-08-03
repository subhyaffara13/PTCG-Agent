from typing import Any, Dict, Optional

def _coerce_metadata_to_dict(value: Any) -> Optional[Dict[str, Any]]:
    """Return ``value`` as a dict, parsing it from JSON if delivered as a string.

    Multipart/form-data and ``extra_body`` callers send ``litellm_metadata``
    as a JSON-encoded string; the proxy parses it into a dict later in
    ``add_litellm_data_to_request``, but the auth-time bouncer runs first
    and would otherwise miss the banned-param check on a still-stringified
    metadata blob.
    """
    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        from litellm.litellm_core_utils.safe_json_loads import safe_json_loads

        parsed = safe_json_loads(value)
        if isinstance(parsed, dict):
            return parsed
    return None

