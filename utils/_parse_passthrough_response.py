
def _parse_passthrough_response(raw_response_obj, coerced_response_obj, kwargs):
    """Return a dict view of the provider response for passthrough routes."""
    # Prefer the coerced view (already JSON-parsed for httpx.Response).
    candidates = []
    if isinstance(coerced_response_obj, dict):
        candidates.append(coerced_response_obj)
    if (
        isinstance(raw_response_obj, dict)
        and raw_response_obj is not coerced_response_obj
    ):
        candidates.append(raw_response_obj)

    for candidate in candidates:
        # StandardPassThroughResponseObject wrapper: {"response": "..."}.
        if (
            "response" in candidate
            and "content" not in candidate
            and "choices" not in candidate
        ):
            inner = candidate.get("response")
            if isinstance(inner, str):
                try:
                    parsed = json.loads(inner)
                    if isinstance(parsed, dict):
                        return parsed
                except Exception:
                    continue
            if isinstance(inner, dict):
                return inner
        else:
            return candidate

    # Fallback: kwargs["original_response"] from the OTel base path.
    original = kwargs.get("original_response") if isinstance(kwargs, dict) else None
    if isinstance(original, dict):
        return original
    if isinstance(original, str):
        try:
            parsed = json.loads(original)
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            return None
    return None

