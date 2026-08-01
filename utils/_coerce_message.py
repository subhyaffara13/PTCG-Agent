
def _coerce_message(detail: Any) -> str:
    """Best-effort, JSON-friendly stringification of an HTTPException-style detail."""
    if detail is None:
        return ""
    if isinstance(detail, str):
        return detail
    if isinstance(detail, Mapping):
        for key in ("error", "message"):
            if isinstance(detail.get(key), str):
                return detail[key]
            inner = detail.get(key)
            if isinstance(inner, Mapping) and isinstance(inner.get("message"), str):
                return inner["message"]
        try:
            return json.dumps(detail)
        except (TypeError, ValueError):
            return str(detail)
    return str(detail)

