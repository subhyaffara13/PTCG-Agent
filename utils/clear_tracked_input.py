
def clear_tracked_input() -> None:
    test_fn = extract_test_fn()
    if test_fn is None:
        return
    if not hasattr(test_fn, "tracked_input"):
        return
    test_fn.tracked_input = None  # type: ignore[attr-defined]

