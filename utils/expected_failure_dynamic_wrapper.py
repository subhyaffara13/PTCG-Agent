
def expectedFailureDynamicWrapper(fn: Callable[_P, _T]) -> Callable[_P, _T]:
    fn._expected_failure_dynamic_wrapper = True  # type: ignore[attr-defined]
    return fn

