from typing import Any, Callable

def wrap_method(
    original_method: Callable[Concatenate[WT, P], Any],
) -> Callable[Concatenate[WT, P], Any]:
    def wrapper(self: WT, /, *args: P.args, **kwargs: P.kwargs) -> Any:
        result = original_method(self, *args, **kwargs)
        if result is NotImplemented:
            return result
        return self._new(result)

    return wrapper


def wrap_method(method):
    """
    Wrap a method as a module so that it can be exported.
    The wrapped module's forward points to the method, and
    the method's original module state is shared.
    """
    if not ismethod(method):
        raise AssertionError(f"Expected {method} to be a method")
    return _WrappedMethod(method)

