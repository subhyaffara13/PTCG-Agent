
def _inplacevar_(op: str, x: Any, y: Any) -> Any:
    # RestrictedPython rewrites ``x += 1`` on a simple name into
    # ``x = _inplacevar_("+=", x, 1)``. The package deliberately ships no
    # default, so we dispatch through ``operator``'s in-place helpers, which
    # honour Python's normal ``__iadd__``/``__add__`` fallback.
    fn = _INPLACE_OPS.get(op)
    if fn is None:
        raise SyntaxError(f"augmented assignment {op!r} is not supported")
    return fn(x, y)

