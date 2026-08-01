
def _is_arbitrary_callable(obj: object) -> bool:
    """
    Returns True if obj is an arbitrary callable (function, lambda, method, etc.)
    that requires special tracing to handle. These cannot be symbolically traced
    using the standard Proxy mechanism.
    """
    import functools
    import types

    return isinstance(
        obj,
        (
            types.FunctionType,
            types.MethodType,
            types.BuiltinFunctionType,
            types.BuiltinMethodType,
            functools.partial,
        ),
    )

