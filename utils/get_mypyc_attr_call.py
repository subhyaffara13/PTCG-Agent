
def get_mypyc_attr_call(d: Expression) -> CallExpr | None:
    """Check if an expression is a call to mypyc_attr and return it if so."""
    if (
        isinstance(d, CallExpr)
        and isinstance(d.callee, RefExpr)
        and d.callee.fullname == "mypy_extensions.mypyc_attr"
    ):
        return d
    return None

