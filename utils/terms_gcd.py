
def terms_gcd(f, *gens, **args):
    """
    Remove GCD of terms from ``f``.

    If the ``deep`` flag is True, then the arguments of ``f`` will have
    terms_gcd applied to them.

    If a fraction is factored out of ``f`` and ``f`` is an Add, then
    an unevaluated Mul will be returned so that automatic simplification
    does not redistribute it. The hint ``clear``, when set to False, can be
    used to prevent such factoring when all coefficients are not fractions.

    Examples
    ========

    >>> from sympy import terms_gcd, cos
    >>> from sympy.abc import x, y
    >>> terms_gcd(x**6*y**2 + x**3*y, x, y)
    x**3*y*(x**3*y + 1)

    The default action of polys routines is to expand the expression
    given to them. terms_gcd follows this behavior:

    >>> terms_gcd((3+3*x)*(x+x*y))
    3*x*(x*y + x + y + 1)

    If this is not desired then the hint ``expand`` can be set to False.
    In this case the expression will be treated as though it were comprised
    of one or more terms:

    >>> terms_gcd((3+3*x)*(x+x*y), expand=False)
    (3*x + 3)*(x*y + x)

    In order to traverse factors of a Mul or the arguments of other
    functions, the ``deep`` hint can be used:

    >>> terms_gcd((3 + 3*x)*(x + x*y), expand=False, deep=True)
    3*x*(x + 1)*(y + 1)
    >>> terms_gcd(cos(x + x*y), deep=True)
    cos(x*(y + 1))

    Rationals are factored out by default:

    >>> terms_gcd(x + y/2)
    (2*x + y)/2

    Only the y-term had a coefficient that was a fraction; if one
    does not want to factor out the 1/2 in cases like this, the
    flag ``clear`` can be set to False:

    >>> terms_gcd(x + y/2, clear=False)
    x + y/2
    >>> terms_gcd(x*y/2 + y**2, clear=False)
    y*(x/2 + y)

    The ``clear`` flag is ignored if all coefficients are fractions:

    >>> terms_gcd(x/3 + y/2, clear=False)
    (2*x + 3*y)/6

    See Also
    ========
    sympy.core.exprtools.gcd_terms, sympy.core.exprtools.factor_terms

    """

    orig = sympify(f)

    if isinstance(f, Equality):
        return Equality(*(terms_gcd(s, *gens, **args) for s in [f.lhs, f.rhs]))
    elif isinstance(f, Relational):
        raise TypeError("Inequalities cannot be used with terms_gcd. Found: %s" %(f,))

    if not isinstance(f, Expr) or f.is_Atom:
        return orig

    if args.get('deep', False):
        new = f.func(*[terms_gcd(a, *gens, **args) for a in f.args])
        args.pop('deep')
        args['expand'] = False
        return terms_gcd(new, *gens, **args)

    clear = args.pop('clear', True)
    options.allowed_flags(args, ['polys'])

    try:
        F, opt = poly_from_expr(f, *gens, **args)
    except PolificationFailed as exc:
        return exc.expr

    J, f = F.terms_gcd()

    if opt.domain.is_Ring:
        if opt.domain.is_Field:
            denom, f = f.clear_denoms(convert=True)

        coeff, f = f.primitive()

        if opt.domain.is_Field:
            coeff /= denom
    else:
        coeff = S.One

    term = Mul(*[x**j for x, j in zip(f.gens, J)])
    if equal_valued(coeff, 1):
        coeff = S.One
        if term == 1:
            return orig

    if clear:
        return _keep_coeff(coeff, term*f.as_expr())
    # base the clearing on the form of the original expression, not
    # the (perhaps) Mul that we have now
    coeff, f = _keep_coeff(coeff, f.as_expr(), clear=False).as_coeff_Mul()
    return _keep_coeff(coeff, term*f, clear=False)

