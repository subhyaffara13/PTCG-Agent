
def get_callable_return_type(
    callable_obj: Any,
    globalns: GlobalsNamespace | None = None,
    localns: MappingNamespace | None = None,
) -> Any | PydanticUndefinedType:
    """Get the callable return type.

    Args:
        callable_obj: The callable to analyze.
        globalns: The globals namespace to use during type annotation evaluation.
        localns: The locals namespace to use during type annotation evaluation.

    Returns:
        The function return type.
    """
    if isinstance(callable_obj, type):
        # types are callables, and we assume the return type
        # is the type itself (e.g. `int()` results in an instance of `int`).
        return callable_obj

    if not isinstance(callable_obj, _function_like):
        call_func = getattr(type(callable_obj), '__call__', None)  # noqa: B004
        if call_func is not None:
            callable_obj = call_func

    hints = get_function_type_hints(
        unwrap_wrapped_function(callable_obj),
        include_keys={'return'},
        globalns=globalns,
        localns=localns,
    )
    return hints.get('return', PydanticUndefined)

