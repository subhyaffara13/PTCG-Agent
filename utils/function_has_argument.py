
def function_has_argument(func: Callable[..., Any], arg_name: str) -> bool:
    """Returns whether or not the given function has a specific parameter"""
    sig = inspect.signature(func)
    return arg_name in sig.parameters


def function_has_argument(function: Callable, arg_name: str) -> bool:
    """Helper function to check if a function has a specific argument."""
    import inspect

    signature = inspect.signature(function)
    return arg_name in signature.parameters

