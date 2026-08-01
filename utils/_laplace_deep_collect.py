
def _laplace_deep_collect(f, t):
    """
    This is an internal helper function that traverses through the expression
    tree of `f(t)` and collects arguments. The purpose of it is that
    anything like `f(w*t-1*t-c)` will be written as `f((w-1)*t-c)` such that
    it can match `f(a*t+b)`.
    """
    if not isinstance(f, Expr):
        return f
    if (p := f.as_poly(t)) is not None:
        return p.as_expr()
    func = f.func
    args = [_laplace_deep_collect(arg, t) for arg in f.args]
    return func(*args)

