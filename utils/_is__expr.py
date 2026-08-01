
def _is_Expr(e):
    """_eapply helper to tell whether ``e`` and all its args
    are Exprs."""
    if isinstance(e, Derivative):
        return _is_Expr(e.expr)
    if not isinstance(e, Expr):
        return False
    return all(_is_Expr(i) for i in e.args)

