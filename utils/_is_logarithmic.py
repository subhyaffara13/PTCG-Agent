
def _is_logarithmic(f, symbol):
    r"""
    Return ``True`` if the equation is in the form
    `a\log(f(x)) + b\log(g(x)) + ... + c` else ``False``.

    Parameters
    ==========

    f : Expr
        The equation to be checked

    symbol : Symbol
        The variable in which the equation is checked

    Returns
    =======

    ``True`` if the equation is logarithmic otherwise ``False``.

    Examples
    ========

    >>> from sympy import symbols, tan, log
    >>> from sympy.solvers.solveset import _is_logarithmic as check
    >>> x, y = symbols('x y')
    >>> check(log(x + 2) - log(x + 3), x)
    True
    >>> check(tan(log(2*x)), x)
    False
    >>> check(x*log(x), x)
    False
    >>> check(x + log(x), x)
    False
    >>> check(y + log(x), x)
    True

    * Philosophy behind the helper

    The function extracts each term and checks whether it is
    logarithmic w.r.t ``symbol``.
    """
    rv = False
    for term in Add.make_args(f):
        saw_log = False
        for term_arg in Mul.make_args(term):
            if symbol not in term_arg.free_symbols:
                continue
            if isinstance(term_arg, log):
                if saw_log:
                    return False  # more than one log in term
                saw_log = True
            else:
                return False  # dependent on symbol in non-log way
        if saw_log:
            rv = True
    return rv

