
def bind_self_fast(method: F, original_type: Type | None = None) -> F:
    """Return a copy of `method`, with the type of its first parameter (usually
    self or cls) bound to original_type.

    This is a faster version of mypy.typeops.bind_self() that can be used for methods
    with trivial self/cls annotations.
    """
    if isinstance(method, Overloaded):
        items = [bind_self_fast(c, original_type) for c in method.items]
        return cast(F, Overloaded(items))
    assert isinstance(method, CallableType)
    if not method.arg_types:
        # Invalid method, return something.
        return method
    if method.arg_kinds[0] in (ARG_STAR, ARG_STAR2):
        # See typeops.py for details.
        return method
    return method.copy_modified(
        arg_types=method.arg_types[1:],
        arg_kinds=method.arg_kinds[1:],
        arg_names=method.arg_names[1:],
        is_bound=True,
    )

