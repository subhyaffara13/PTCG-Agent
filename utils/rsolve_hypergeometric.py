
def rsolve_hypergeometric(f, x, P, Q, k, m):
    """
    Solves RE of hypergeometric type.

    Explanation
    ===========

    Attempts to solve RE of the form

    Q(k)*a(k + m) - P(k)*a(k)

    Transformations that preserve Hypergeometric type:

        a. x**n*f(x): b(k + m) = R(k - n)*b(k)
        b. f(A*x): b(k + m) = A**m*R(k)*b(k)
        c. f(x**n): b(k + n*m) = R(k/n)*b(k)
        d. f(x**(1/m)): b(k + 1) = R(k*m)*b(k)
        e. f'(x): b(k + m) = ((k + m + 1)/(k + 1))*R(k + 1)*b(k)

    Some of these transformations have been used to solve the RE.

    Returns
    =======

    formula : Expr
    ind : Expr
        Independent terms.
    order : int

    Examples
    ========

    >>> from sympy import exp, ln, S
    >>> from sympy.series.formal import rsolve_hypergeometric as rh
    >>> from sympy.abc import x, k

    >>> rh(exp(x), x, -S.One, (k + 1), k, 1)
    (Piecewise((1/factorial(k), Eq(Mod(k, 1), 0)), (0, True)), 1, 1)

    >>> rh(ln(1 + x), x, k**2, k*(k + 1), k, 1)
    (Piecewise(((-1)**(k - 1)*factorial(k - 1)/RisingFactorial(2, k - 1),
     Eq(Mod(k, 1), 0)), (0, True)), x, 2)

    References
    ==========

    .. [1] Formal Power Series - Dominik Gruntz, Wolfram Koepf
    .. [2] Power Series in Computer Algebra - Wolfram Koepf
    """
    result = _rsolve_hypergeometric(f, x, P, Q, k, m)

    if result is None:
        return None

    sol_list, ind, mp = result

    sol_dict = defaultdict(lambda: S.Zero)
    for res, cond in sol_list:
        j, mk = cond.as_coeff_Add()
        c = mk.coeff(k)

        if j.is_integer is False:
            res *= x**frac(j)
            j = floor(j)

        res = res.subs(k, (k - j) / c)
        cond = Eq(k % c, j % c)
        sol_dict[cond] += res  # Group together formula for same conditions

    sol = [(res, cond) for cond, res in sol_dict.items()]
    sol.append((S.Zero, True))
    sol = Piecewise(*sol)

    if mp is -oo:
        s = S.Zero
    elif mp.is_integer is False:
        s = ceiling(mp)
    else:
        s = mp + 1

    #  save all the terms of
    #  form 1/x**k in ind
    if s < 0:
        ind += sum(sequence(sol * x**k, (k, s, -1)))
        s = S.Zero

    return (sol, ind, s)

