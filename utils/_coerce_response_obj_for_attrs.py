
def _coerce_response_obj_for_attrs(response_obj):
    """Return a `.get`-compatible view of `response_obj` when possible.

    - dicts and Pydantic models that already expose `.get` are returned
      unchanged (preserves all current behavior, including the Responses API
      flow which relies on Pydantic attribute access).
    - `httpx.Response` and other text-only responses (passthrough routes)
      are JSON-decoded so the standard extraction paths can read fields like
      `id`, `model`, and `usage`. On failure the original object is returned
      so behavior is no worse than today.
    """
    if response_obj is None or hasattr(response_obj, "get"):
        return response_obj
    text = getattr(response_obj, "text", None)
    if isinstance(text, str) and text:
        try:
            parsed = json.loads(text)
            if isinstance(parsed, dict):
                return parsed
        except Exception:
            pass
    return response_obj

