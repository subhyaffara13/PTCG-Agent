from typing import Any, Callable

def dont_skip_tracing(fn: None = None) -> DynamoConfigPatchProxy: ...


def dont_skip_tracing(fn: Callable[_P, _R]) -> Callable[_P, _R]: ...


def dont_skip_tracing(fn: Any | None = None) -> Any:
    """
    Context manager/decorator to trace into functions intentionally marked by developers to be skipped
    when tracing.

    This decorator will also apply to recursively invoked functions.
    """
    ctx = patch_dynamo_config(dont_skip_tracing=True)
    if fn:
        return ctx(fn)
    return ctx

