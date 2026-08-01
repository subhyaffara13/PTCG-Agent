
def symmetrize(x):
    "Make layer symmetric in final two dimensions, used for contact prediction."
    return x + x.transpose(-1, -2)


def symmetrize(F, *gens, **args):
    r"""
    Rewrite a polynomial in terms of elementary symmetric polynomials.

    A symmetric polynomial is a multivariate polynomial that remains invariant
    under any variable permutation, i.e., if `f = f(x_1, x_2, \dots, x_n)`,
    then `f = f(x_{i_1}, x_{i_2}, \dots, x_{i_n})`, where
    `(i_1, i_2, \dots, i_n)` is a permutation of `(1, 2, \dots, n)` (an
    element of the group `S_n`).

    Returns a tuple of symmetric polynomials ``(f1, f2, ..., fn)`` such that
    ``f = f1 + f2 + ... + fn``.

    Examples
    ========

    >>> from sympy.polys.polyfuncs import symmetrize
    >>> from sympy.abc import x, y

    >>> symmetrize(x**2 + y**2)
    (-2*x*y + (x + y)**2, 0)

    >>> symmetrize(x**2 + y**2, formal=True)
    (s1**2 - 2*s2, 0, [(s1, x + y), (s2, x*y)])

    >>> symmetrize(x**2 - y**2)
    (-2*x*y + (x + y)**2, -2*y**2)

    >>> symmetrize(x**2 - y**2, formal=True)
    (s1**2 - 2*s2, -2*y**2, [(s1, x + y), (s2, x*y)])

    """
    allowed_flags(args, ['formal', 'symbols'])

    iterable = True

    if not hasattr(F, '__iter__'):
        iterable = False
        F = [F]

    R, F = sring(F, *gens, **args)
    gens = R.symbols

    opt = build_options(gens, args)
    symbols = opt.symbols
    symbols = [next(symbols) for i in range(len(gens))]

    result = []

    for f in F:
        p, r, m = f.symmetrize()
        result.append((p.as_expr(*symbols), r.as_expr(*gens)))

    polys = [(s, g.as_expr()) for s, (_, g) in zip(symbols, m)]

    if not opt.formal:
        for i, (sym, non_sym) in enumerate(result):
            result[i] = (sym.subs(polys), non_sym)

    if not iterable:
        result, = result

    if not opt.formal:
        return result
    else:
        if iterable:
            return result, polys
        else:
            return result + (polys,)


def symmetrize(x: Array) -> Array: return (x + _H(x)) / 2

