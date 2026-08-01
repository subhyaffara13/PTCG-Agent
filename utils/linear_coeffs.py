
def linear_coeffs(eq, *syms, dict=False):
    """Return a list whose elements are the coefficients of the
    corresponding symbols in the sum of terms in  ``eq``.
    The additive constant is returned as the last element of the
    list.

    Raises
    ======

    NonlinearError
        The equation contains a nonlinear term
    ValueError
        duplicate or unordered symbols are passed

    Parameters
    ==========

    dict - (default False) when True, return coefficients as a
        dictionary with coefficients keyed to syms that were present;
        key 1 gives the constant term

    Examples
    ========

    >>> from sympy.solvers.solveset import linear_coeffs
    >>> from sympy.abc import x, y, z
    >>> linear_coeffs(3*x + 2*y - 1, x, y)
    [3, 2, -1]

    It is not necessary to expand the expression:

        >>> linear_coeffs(x + y*(z*(x*3 + 2) + 3), x)
        [3*y*z + 1, y*(2*z + 3)]

    When nonlinear is detected, an error will be raised:

        * even if they would cancel after expansion (so the
        situation does not pass silently past the caller's
        attention)

        >>> eq = 1/x*(x - 1) + 1/x
        >>> linear_coeffs(eq.expand(), x)
        [0, 1]
        >>> linear_coeffs(eq, x)
        Traceback (most recent call last):
        ...
        NonlinearError:
        nonlinear in given generators

        * when there are cross terms

        >>> linear_coeffs(x*(y + 1), x, y)
        Traceback (most recent call last):
        ...
        NonlinearError:
        symbol-dependent cross-terms encountered

        * when there are terms that contain an expression
        dependent on the symbols that is not linear

        >>> linear_coeffs(x**2, x)
        Traceback (most recent call last):
        ...
        NonlinearError:
        nonlinear in given generators
    """
    eq = _sympify(eq)
    if len(syms) == 1 and iterable(syms[0]) and not isinstance(syms[0], Basic):
        raise ValueError('expecting unpacked symbols, *syms')
    symset = set(syms)
    if len(symset) != len(syms):
        raise ValueError('duplicate symbols given')
    try:
        d, c = _linear_eq_to_dict([eq], symset)
        d = d[0]
        c = c[0]
    except PolyNonlinearError as err:
        raise NonlinearError(str(err))
    if dict:
        if c:
            d[S.One] = c
        return d
    rv = [S.Zero]*(len(syms) + 1)
    rv[-1] = c
    for i, k in enumerate(syms):
        if k not in d:
            continue
        rv[i] = d[k]
    return rv

