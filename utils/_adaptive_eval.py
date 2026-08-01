
def _adaptive_eval(f, x):
    """Evaluate f(x) with an adaptive algorithm. Post-process the result.
    If a symbolic expression is evaluated with SymPy, it might returns
    another symbolic expression, containing additions, ...
    Force evaluation to a float.

    Parameters
    ==========
    f : callable
    x : float
    """
    np = import_module('numpy')

    y = f(x)
    if isinstance(y, Expr) and (not y.is_Number):
        y = y.evalf()
    y = complex(y)
    if y.imag > 1e-08:
        return np.nan
    return y.real

