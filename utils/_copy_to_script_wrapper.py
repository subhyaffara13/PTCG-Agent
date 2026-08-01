
def _copy_to_script_wrapper(fn: Callable[_P, _R]) -> Callable[_P, _R]:
    fn._torchscript_modifier = FunctionModifiers.COPY_TO_SCRIPT_WRAPPER  # type: ignore[attr-defined]
    return fn

