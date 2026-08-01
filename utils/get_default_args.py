
def get_default_args(fn):
    """
    Get a dictionary of default arguments for a function.

    Args:
        fn: Callable - The function to inspect for default arguments.
    Returns:
        (Dict[str, Any]): mapping argument names to their default values if
        :attr:`fn` is not None, else empty dictionary.
    """
    if fn is None:
        return {}

    signature = inspect.signature(fn)

    return {
        k: v.default
        for k, v in signature.parameters.items()
        if v.default is not inspect.Parameter.empty
    }

