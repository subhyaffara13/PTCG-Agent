from typing import Any, Callable

def disable_nested_graph_breaks(fn: None = None) -> DynamoConfigPatchProxy: ...


def disable_nested_graph_breaks(fn: Callable[_P, _R]) -> Callable[_P, _R]: ...


def disable_nested_graph_breaks(fn: Any | None = None) -> Any:
    """
    Context manager/decorator to disable nested graph breaks when tracing
    this function and any nested functions. Used when nested graph breaks
    is causing problems.
    """
    ctx = patch_dynamo_config(nested_graph_breaks=False)
    if fn:
        return ctx(fn)
    return ctx

