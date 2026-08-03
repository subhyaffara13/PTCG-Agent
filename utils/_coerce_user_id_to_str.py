from typing import Any, Optional

def _coerce_user_id_to_str(value: Any) -> Optional[str]:
    """Return a usable end-user identifier string, or None if the value isn't one.

    Always drops non-string structured values (dict/list/tuple/set) because
    stringifying them produces garbage spend-log rows like
    ``"{'device_id': ...}"``. Strings that *decode* to a structured payload
    are only rejected when ``litellm.validate_end_user_id_in_db`` is enabled
    — operators who currently pass JSON-encoded identifiers keep their
    existing behavior until they opt in. See
    auth_utils.py:get_end_user_id_from_request_body for the extraction chain.
    """
    if value is None:
        return None
    if isinstance(value, bool):
        # bool is an int subclass; handle explicitly to avoid "True"/"False".
        return None
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, str):
        stripped = value.strip()
        if not stripped:
            return None
        # Reject strings that decode to a structured payload (JSON object/array)
        # only when the operator has opted into end-user validation. Gating
        # behind the flag preserves backwards compatibility for deployments
        # that intentionally pass JSON-encoded user identifiers.
        if litellm.validate_end_user_id_in_db and stripped[:1] in ("{", "["):
            parsed = safe_json_loads(stripped)
            if isinstance(parsed, (dict, list)):
                return None
        return stripped
    # dict, list, tuple, set, arbitrary objects -> drop.
    return None

