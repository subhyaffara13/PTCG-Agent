
def disable(fn=None, recursive=True, *, reason=None):
    """
    This function provides a decorator to disable compilation on a function.
    It also provides the option of recursively disabling called functions.

    Args:
        fn (optional): The function to disable
        recursive (optional): A boolean value indicating whether the disabling should be recursive.
        reason (optional): A string value indicating the reason for disabling the function.
    """
    import torch._dynamo

    return torch._dynamo.disable(fn, recursive, reason=reason)


def disable() -> None:
    _enabled.enabled = False


def disable(fn=None, recursive=True, *, reason=None, wrapping=True):  # type: ignore[no-untyped-def]
    """
    Decorator to disable TorchDynamo

    If recursive=True, Dynamo is completely skipped on the decorated function
    frame as well as the recursively invoked functions.

    If recursive=False, Dynamo skips frames associated with the function code,
    but still process recursively invoked frames.

    If reason is provided, it will be printed when Dynamo attempts to trace the disabled function.
    """
    if recursive:
        if fn is not None:
            fn = innermost_fn(fn)
            assert callable(fn)
            return DisableContext(msg=reason, wrapping=wrapping)(fn)
        return DisableContext(msg=reason, wrapping=wrapping)
    else:

        def wrap(fn: Callable[_P, _R]) -> Callable[_P, _R]:
            fn = innermost_fn(fn)
            assert callable(fn)

            nonrecursive_disable_wrapper = get_nonrecursive_disable_wrapper(fn)
            nonrecursive_disable_wrapper._torchdynamo_disable = True  # type: ignore[attr-defined]
            nonrecursive_disable_wrapper._torchdynamo_disable_msg = reason  # type: ignore[attr-defined]
            nonrecursive_disable_wrapper._torchdynamo_orig_callable = fn  # type: ignore[attr-defined]
            nonrecursive_disable_wrapper._torchdynamo_wrapper_id = id(  # type: ignore[attr-defined]
                nonrecursive_disable_wrapper
            )
            nonrecursive_disable_wrapper._torchdynamo_disable_recursive = False  # type: ignore[attr-defined]
            return nonrecursive_disable_wrapper

        if fn is None:
            return wrap
        return wrap(fn)

