
def _invert(eq, *symbols, **kwargs):
    """
    Return tuple (i, d) where ``i`` is independent of *symbols* and ``d``
    contains symbols.

    Explanation
    ===========

    ``i`` and ``d`` are obtained after recursively using algebraic inversion
    until an uninvertible ``d`` remains. If there are no free symbols then
    ``d`` will be zero. Some (but not necessarily all) solutions to the
    expression ``i - d`` will be related to the solutions of the original
    expression.

    Examples
    ========

    >>> from sympy.solvers.solvers import _invert as invert
    >>> from sympy import sqrt, cos
    >>> from sympy.abc import x, y
    >>> invert(x - 3)
    (3, x)
    >>> invert(3)
    (3, 0)
    >>> invert(2*cos(x) - 1)
    (1/2, cos(x))
    >>> invert(sqrt(x) - 3)
    (3, sqrt(x))
    >>> invert(sqrt(x) + y, x)
    (-y, sqrt(x))
    >>> invert(sqrt(x) + y, y)
    (-sqrt(x), y)
    >>> invert(sqrt(x) + y, x, y)
    (0, sqrt(x) + y)

    If there is more than one symbol in a power's base and the exponent
    is not an Integer, then the principal root will be used for the
    inversion:

    >>> invert(sqrt(x + y) - 2)
    (4, x + y)
    >>> invert(sqrt(x + y) + 2)  # note +2 instead of -2
    (4, x + y)

    If the exponent is an Integer, setting ``integer_power`` to True
    will force the principal root to be selected:

    >>> invert(x**2 - 4, integer_power=True)
    (2, x)

    """
    eq = sympify(eq)
    if eq.args:
        # make sure we are working with flat eq
        eq = eq.func(*eq.args)
    free = eq.free_symbols
    if not symbols:
        symbols = free
    if not free & set(symbols):
        return eq, S.Zero

    dointpow = bool(kwargs.get('integer_power', False))

    lhs = eq
    rhs = S.Zero
    while True:
        was = lhs
        while True:
            indep, dep = lhs.as_independent(*symbols)

            # dep + indep == rhs
            if lhs.is_Add:
                # this indicates we have done it all
                if indep.is_zero:
                    break

                lhs = dep
                rhs -= indep

            # dep * indep == rhs
            else:
                # this indicates we have done it all
                if indep is S.One:
                    break

                lhs = dep
                rhs /= indep

        # collect like-terms in symbols
        if lhs.is_Add:
            terms = {}
            for a in lhs.args:
                i, d = a.as_independent(*symbols)
                terms.setdefault(d, []).append(i)
            if any(len(v) > 1 for v in terms.values()):
                args = []
                for d, i in terms.items():
                    if len(i) > 1:
                        args.append(Add(*i)*d)
                    else:
                        args.append(i[0]*d)
                lhs = Add(*args)

        # if it's a two-term Add with rhs = 0 and two powers we can get the
        # dependent terms together, e.g. 3*f(x) + 2*g(x) -> f(x)/g(x) = -2/3
        if lhs.is_Add and not rhs and len(lhs.args) == 2 and \
                not lhs.is_polynomial(*symbols):
            a, b = ordered(lhs.args)
            ai, ad = a.as_independent(*symbols)
            bi, bd = b.as_independent(*symbols)
            if any(_ispow(i) for i in (ad, bd)):
                a_base, a_exp = ad.as_base_exp()
                b_base, b_exp = bd.as_base_exp()
                if a_base == b_base and a_exp.extract_additively(b_exp) is None:
                    # a = -b and exponents do not have canceling terms/factors
                    # e.g. if exponents were 3*x and x then the ratio would have
                    # an exponent of 2*x: one of the roots would be lost
                    rat = powsimp(powdenest(ad/bd))
                    lhs = rat
                    rhs = -bi/ai
                else:
                    rat = ad/bd
                    _lhs = powsimp(ad/bd)
                    if _lhs != rat:
                        lhs = _lhs
                        rhs = -bi/ai
            elif ai == -bi:
                if isinstance(ad, Function) and ad.func == bd.func:
                    if len(ad.args) == len(bd.args) == 1:
                        lhs = ad.args[0] - bd.args[0]
                    elif len(ad.args) == len(bd.args):
                        # should be able to solve
                        # f(x, y) - f(2 - x, 0) == 0 -> x == 1
                        raise NotImplementedError(
                            'equal function with more than 1 argument')
                    else:
                        raise ValueError(
                            'function with different numbers of args')

        elif lhs.is_Mul and any(_ispow(a) for a in lhs.args):
            lhs = powsimp(powdenest(lhs))

        if lhs.is_Function:
            if hasattr(lhs, 'inverse') and lhs.inverse() is not None and len(lhs.args) == 1:
                #                    -1
                # f(x) = g  ->  x = f  (g)
                #
                # /!\ inverse should not be defined if there are multiple values
                # for the function -- these are handled in _tsolve
                #
                rhs = lhs.inverse()(rhs)
                lhs = lhs.args[0]
            elif isinstance(lhs, atan2):
                y, x = lhs.args
                lhs = 2*atan(y/(sqrt(x**2 + y**2) + x))
            elif lhs.func == rhs.func:
                if len(lhs.args) == len(rhs.args) == 1:
                    lhs = lhs.args[0]
                    rhs = rhs.args[0]
                elif len(lhs.args) == len(rhs.args):
                    # should be able to solve
                    # f(x, y) == f(2, 3) -> x == 2
                    # f(x, x + y) == f(2, 3) -> x == 2
                    raise NotImplementedError(
                        'equal function with more than 1 argument')
                else:
                    raise ValueError(
                        'function with different numbers of args')


        if rhs and lhs.is_Pow and lhs.exp.is_Integer and lhs.exp < 0:
            lhs = 1/lhs
            rhs = 1/rhs

        # base**a = b -> base = b**(1/a) if
        #    a is an Integer and dointpow=True (this gives real branch of root)
        #    a is not an Integer and the equation is multivariate and the
        #      base has more than 1 symbol in it
        # The rationale for this is that right now the multi-system solvers
        # doesn't try to resolve generators to see, for example, if the whole
        # system is written in terms of sqrt(x + y) so it will just fail, so we
        # do that step here.
        if lhs.is_Pow and (
            lhs.exp.is_Integer and dointpow or not lhs.exp.is_Integer and
                len(symbols) > 1 and len(lhs.base.free_symbols & set(symbols)) > 1):
            rhs = rhs**(1/lhs.exp)
            lhs = lhs.base

        if lhs == was:
            break
    return rhs, lhs


def _invert(f_x, y, x, domain=S.Complexes):
    r"""
    Reduce the complex valued equation $f(x) = y$ to a set of equations

    $$\left\{g(x) = h_1(y),\  g(x) = h_2(y),\ \dots,\  g(x) = h_n(y) \right\}$$

    where $g(x)$ is a simpler function than $f(x)$.  The return value is a tuple
    $(g(x), \mathrm{set}_h)$, where $g(x)$ is a function of $x$ and $\mathrm{set}_h$ is
    the set of function $\left\{h_1(y), h_2(y), \dots, h_n(y)\right\}$.
    Here, $y$ is not necessarily a symbol.

    $\mathrm{set}_h$ contains the functions, along with the information
    about the domain in which they are valid, through set
    operations. For instance, if :math:`y = |x| - n` is inverted
    in the real domain, then $\mathrm{set}_h$ is not simply
    $\{-n, n\}$ as the nature of `n` is unknown; rather, it is:

    $$ \left(\left[0, \infty\right) \cap \left\{n\right\}\right) \cup
                       \left(\left(-\infty, 0\right] \cap \left\{- n\right\}\right)$$

    By default, the complex domain is used which means that inverting even
    seemingly simple functions like $\exp(x)$ will give very different
    results from those obtained in the real domain.
    (In the case of $\exp(x)$, the inversion via $\log$ is multi-valued
    in the complex domain, having infinitely many branches.)

    If you are working with real values only (or you are not sure which
    function to use) you should probably set the domain to
    ``S.Reals`` (or use ``invert_real`` which does that automatically).


    Examples
    ========

    >>> from sympy.solvers.solveset import invert_complex, invert_real
    >>> from sympy.abc import x, y
    >>> from sympy import exp

    When does exp(x) == y?

    >>> invert_complex(exp(x), y, x)
    (x, ImageSet(Lambda(_n, I*(2*_n*pi + arg(y)) + log(Abs(y))), Integers))
    >>> invert_real(exp(x), y, x)
    (x, Intersection({log(y)}, Reals))

    When does exp(x) == 1?

    >>> invert_complex(exp(x), 1, x)
    (x, ImageSet(Lambda(_n, 2*_n*I*pi), Integers))
    >>> invert_real(exp(x), 1, x)
    (x, {0})

    See Also
    ========
    invert_real, invert_complex
    """
    x = sympify(x)
    if not x.is_Symbol:
        raise ValueError("x must be a symbol")
    f_x = sympify(f_x)
    if x not in f_x.free_symbols:
        raise ValueError("Inverse of constant function doesn't exist")
    y = sympify(y)
    if x in y.free_symbols:
        raise ValueError("y should be independent of x ")

    if domain.is_subset(S.Reals):
        x1, s = _invert_real(f_x, FiniteSet(y), x)
    else:
        x1, s = _invert_complex(f_x, FiniteSet(y), x)

    # f couldn't be inverted completely; return unmodified.
    if  x1 != x:
        return x1, s

    # Avoid adding gratuitous intersections with S.Complexes. Actual
    # conditions should be handled by the respective inverters.
    if domain is S.Complexes:
        return x1, s

    if isinstance(s, FiniteSet):
        return x1, s.intersect(domain)

    # "Fancier" solution sets like those obtained by inversion of trigonometric
    # functions already include general validity conditions (i.e. conditions on
    # the domain of the respective inverse functions), so we should avoid adding
    # blanket intersections with S.Reals. But subsets of R (or C) must still be
    # accounted for.
    if domain is S.Reals:
        return x1, s
    else:
        return x1, s.intersect(domain)

