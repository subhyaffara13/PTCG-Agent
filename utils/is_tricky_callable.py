
def is_tricky_callable(t: CallableType) -> bool:
    """Is t a callable that we need to put a ... in for syntax reasons?"""
    return t.is_ellipsis_args or any(k.is_star() or k.is_named() for k in t.arg_kinds)

