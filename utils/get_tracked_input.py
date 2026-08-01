
def get_tracked_input() -> TrackedInput | None:
    test_fn = extract_test_fn()
    if test_fn is None:
        return None
    return getattr(test_fn, "tracked_input", None)

