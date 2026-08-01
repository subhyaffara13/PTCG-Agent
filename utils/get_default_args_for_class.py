
def get_default_args_for_class(cls):
    """
    Get default arguments for all methods in a class (except for static methods).

    Args:
        cls: type - The class type to inspect for default arguments.
    Returns:
        A Dict[str, Dict[str, Any]] which maps each method name to a Dict[str, Any]
        that maps each argument name to its default value.
    """
    # Get methods (except static methods because those are compiled separately as
    # if they were independent script functions).
    methods = inspect.getmembers(
        cls,
        predicate=lambda m: (inspect.ismethod(m) or inspect.isfunction(m))
        and not is_static_fn(cls, m.__name__)
        and m.__name__ in cls.__dict__,
    )

    # Get method defaults. Property defaults do not need to be considered
    # because setters cannot be invoked without a value.
    defaults = {
        method_name: get_default_args(method_impl)
        for method_name, method_impl in methods
    }

    return defaults

