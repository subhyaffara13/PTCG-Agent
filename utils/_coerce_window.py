
def _coerce_window(window: Any) -> dict:
    if isinstance(window, dict):
        return window
    if isinstance(window, str):
        try:
            parsed = json.loads(window)
            return parsed if isinstance(parsed, dict) else {}
        except Exception:
            return {}
    if hasattr(window, "model_dump"):
        return window.model_dump()
    return {}

