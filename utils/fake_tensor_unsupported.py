
def fake_tensor_unsupported(fn: Callable[[Any, list[Any], Any], R]) -> Any:
    """
    Decorator for backends that need real inputs.  We swap out fake
    tensors for zero tensors.
    """

    @functools.wraps(fn)
    def wrapper(model: Any, inputs: Any, **kwargs: Any) -> Any:
        with _disable_current_modes():
            inputs = list(map(defake, inputs))
            return fn(model, inputs, **kwargs)  # type: ignore[call-arg]

    return wrapper

