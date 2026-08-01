
def get_required_world_size(obj: Any, default: int) -> int:
    """
    Returns the requested world size for the currently running unittest method on `obj`
    if annotated via `@require_world_size(n)`, else returns `default`.
    """
    try:
        # Try MultiProcessTestCase helper first, then unittest fallback
        test_name = (
            obj._current_test_name()  # type: ignore[attr-defined]
            if hasattr(obj, "_current_test_name") and callable(obj._current_test_name)
            else obj._testMethodName
        )
        fn = getattr(obj, test_name)
        value = fn._required_world_size
        return int(value)
    except Exception:
        return default

