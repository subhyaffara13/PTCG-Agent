
def refine_callable(t: CallableType, s: CallableType) -> CallableType:
    """Refine a callable based on another.

    See comments for refine_type.
    """
    if t.fallback != s.fallback:
        return t

    if t.is_ellipsis_args and not is_tricky_callable(s):
        return s.copy_modified(ret_type=refine_type(t.ret_type, s.ret_type))

    if is_tricky_callable(t) or t.arg_kinds != s.arg_kinds:
        return t

    return t.copy_modified(
        arg_types=[refine_type(ta, sa) for ta, sa in zip(t.arg_types, s.arg_types)],
        ret_type=refine_type(t.ret_type, s.ret_type),
    )

