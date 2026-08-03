from typing import Any, Callable

def annotate_fn(
    annotation_dict: dict[str, Any],
) -> Callable[[Callable[_P, _R]], Callable[_P, _R]]:
    """
    A decorator that wraps a function with the annotate context manager.
    Use this when you want to annotate an entire function instead of a specific code block.

    Note:
        This API is **not backward compatible** and may evolve in future releases.

    Note:
        This API is not compatible with fx.symbolic_trace or jit.trace. It's intended
        to be used with PT2 family of tracers, e.g. torch.export and dynamo.

    Args:
        annotation_dict (dict): A dictionary of custom key-value pairs to inject
            into the FX trace metadata for all operations in the function.

    Example:
        All operations in my_function will have {"pp_stage": 1} in their metadata.

        >>> @annotate_fn({"pp_stage": 1})
        ... def my_function(x):
        ...     return x + 1
    """
    from functools import wraps

    def decorator(func: Callable[_P, _R]) -> Callable[_P, _R]:
        @wraps(func)
        # NB: Do not annotate with _P.args/_P.kwargs here. Dynamo guards on
        # the identity of ParamSpec annotation objects, causing guard failures.
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            with annotate(annotation_dict):
                return func(*args, **kwargs)

        return wrapper  # type: ignore[return-value]

    return decorator

