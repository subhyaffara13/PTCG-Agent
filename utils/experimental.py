
def experimental(cls):
    """
    Decorator to mark a class as experimental.
    """
    original_init = cls.__init__

    @wraps(original_init)
    def new_init(self, *args, **kwargs):
        warnings.warn(
            f"{cls.__name__} is an experimental and may change or be removed in future versions.",
            category=UserWarning,
            stacklevel=2,
        )
        original_init(self, *args, **kwargs)

    cls.__init__ = new_init
    return cls


def experimental(fn: Callable) -> Callable:
    """Decorator to flag a feature as experimental.

    An experimental feature triggers a warning when used as it might be subject to breaking changes without prior notice
    in the future.

    Warnings can be disabled by setting `HF_HUB_DISABLE_EXPERIMENTAL_WARNING=1` as environment variable.

    Args:
        fn (`Callable`):
            The function to flag as experimental.

    Returns:
        `Callable`: The decorated function.

    Example:

    ```python
    >>> from huggingface_hub.utils import experimental

    >>> @experimental
    ... def my_function():
    ...     print("Hello world!")

    >>> my_function()
    UserWarning: 'my_function' is experimental and might be subject to breaking changes in the future without prior
    notice. You can disable this warning by setting `HF_HUB_DISABLE_EXPERIMENTAL_WARNING=1` as environment variable.
    Hello world!
    ```
    """
    # For classes, put the "experimental" around the "__new__" method => __new__ will be removed in warning message
    name = fn.__qualname__[: -len(".__new__")] if fn.__qualname__.endswith(".__new__") else fn.__qualname__

    @wraps(fn)
    def _inner_fn(*args, **kwargs):
        if not constants.HF_HUB_DISABLE_EXPERIMENTAL_WARNING:
            warnings.warn(
                f"'{name}' is experimental and might be subject to breaking changes in the future without prior notice."
                " You can disable this warning by setting `HF_HUB_DISABLE_EXPERIMENTAL_WARNING=1` as environment"
                " variable.",
                UserWarning,
            )
        return fn(*args, **kwargs)

    return _inner_fn

