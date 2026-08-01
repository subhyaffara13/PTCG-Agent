
def expectedFailureCodegenDynamic(fn: Callable[_P, _T]) -> Callable[_P, _T]:
    fn._expected_failure_codegen_dynamic = True  # type: ignore[attr-defined]
    return fn

