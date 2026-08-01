
def _is_fallback_handler(op: object) -> bool:
    try:
        return op._is_fallback_handler  # type: ignore[attr-defined]
    except AttributeError:
        return False

