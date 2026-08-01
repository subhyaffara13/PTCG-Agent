
def _drop(fn: Callable[_P, _R]) -> Callable[_P, _R]:
    fn._torchscript_modifier = FunctionModifiers._DROP  # type: ignore[attr-defined]
    return fn

