
def set_module(obj, mod):
    """
    Set the module attribute on a python object for a given object for nicer printing
    """
    if not isinstance(mod, str):
        raise TypeError("The mod argument should be a string")
    obj.__module__ = mod


def set_module(module) -> Callable[[F], F]:
    """Private decorator for overriding __module__ on a function or class.

    Example usage::

        @set_module("pandas")
        def example():
            pass


        assert example.__module__ == "pandas"
    """

    def decorator(func: F) -> F:
        if module is not None:
            if isinstance(func, type):
                # Store the original module for classes to ensure linkcode_resolve
                # can resolve the true source location after re-exporting
                try:
                    func._module_source = func.__module__  # type: ignore[attr-defined]
                except AttributeError:
                    pass

            func.__module__ = module
        return cast("F", func)  # type: ignore[redundant-cast]

    return decorator


def set_module(module):
    """Private decorator for overriding __module__ on a function or class.

    Example usage::

        @set_module('numpy')
        def example():
            pass

        assert example.__module__ == 'numpy'
    """
    def decorator(func):
        if module is not None:
            if isinstance(func, type):
                try:
                    func._module_source = func.__module__
                except (AttributeError):
                    pass

            func.__module__ = module
        return func
    return decorator


def set_module(module: str) -> Callable[[T], T]:
  def wrapper(func: T) -> T:
    if module is not None:
      func.__module__ = module
    return func
  return wrapper

