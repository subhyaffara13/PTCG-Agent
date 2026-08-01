
def _is_lambert(f, symbol):
    r"""
    If this returns ``False`` then the Lambert solver (``_solve_lambert``) will not be called.

    Explanation
    ===========

    Quick check for cases that the Lambert solver might be able to handle.

    1. Equations containing more than two operands and `symbol`s involving any of
       `Pow`, `exp`, `HyperbolicFunction`,`TrigonometricFunction`, `log` terms.

    2. In `Pow`, `exp` the exponent should have `symbol` whereas for
       `HyperbolicFunction`,`TrigonometricFunction`, `log` should contain `symbol`.

    3. For `HyperbolicFunction`,`TrigonometricFunction` the number of trigonometric functions in
       equation should be less than number of symbols. (since `A*cos(x) + B*sin(x) - c`
       is not the Lambert type).

    Some forms of lambert equations are:
        1. X**X = C
        2. X*(B*log(X) + D)**A = C
        3. A*log(B*X + A) + d*X = C
        4. (B*X + A)*exp(d*X + g) = C
        5. g*exp(B*X + h) - B*X = C
        6. A*D**(E*X + g) - B*X = C
        7. A*cos(X) + B*sin(X) - D*X = C
        8. A*cosh(X) + B*sinh(X) - D*X = C

    Where X is any variable,
          A, B, C, D, E are any constants,
          g, h are linear functions or log terms.

    Parameters
    ==========

    f : Expr
        The equation to be checked

    symbol : Symbol
        The variable in which the equation is checked

    Returns
    =======

    If this returns ``False`` then the Lambert solver (``_solve_lambert``) will not be called.

    Examples
    ========

    >>> from sympy.solvers.solveset import _is_lambert
    >>> from sympy import symbols, cosh, sinh, log
    >>> x = symbols('x')

    >>> _is_lambert(3*log(x) - x*log(3), x)
    True
    >>> _is_lambert(log(log(x - 3)) + log(x-3), x)
    True
    >>> _is_lambert(cosh(x) - sinh(x), x)
    False
    >>> _is_lambert((x**2 - 2*x + 1).subs(x, (log(x) + 3*x)**2 - 1), x)
    True

    See Also
    ========

    _solve_lambert

    """
    term_factors = list(_term_factors(f.expand()))

    # total number of symbols in equation
    no_of_symbols = len([arg for arg in term_factors if arg.has(symbol)])
    # total number of trigonometric terms in equation
    no_of_trig = len([arg for arg in term_factors \
        if arg.has(HyperbolicFunction, TrigonometricFunction)])

    if f.is_Add and no_of_symbols >= 2:
        # `log`, `HyperbolicFunction`, `TrigonometricFunction` should have symbols
        # and no_of_trig < no_of_symbols
        lambert_funcs = (log, HyperbolicFunction, TrigonometricFunction)
        if any(isinstance(arg, lambert_funcs)\
            for arg in term_factors if arg.has(symbol)):
                if no_of_trig < no_of_symbols:
                    return True
        # here, `Pow`, `exp` exponent should have symbols
        elif any(isinstance(arg, (Pow, exp)) \
            for arg in term_factors if (arg.as_base_exp()[1]).has(symbol)):
            return True
    return False

