
def _meijerint_indefinite_1(f, x):
    """ Helper that does not attempt any substitution. """
    _debug('Trying to compute the indefinite integral of', f, 'wrt', x)
    from sympy.simplify import hyperexpand, powdenest

    gs = _rewrite1(f, x)
    if gs is None:
        # Note: the code that calls us will do expand() and try again
        return None

    fac, po, gl, cond = gs
    _debug(' could rewrite:', gs)
    res = S.Zero
    for C, s, g in gl:
        a, b = _get_coeff_exp(g.argument, x)
        _, c = _get_coeff_exp(po, x)
        c += s

        # we do a substitution t=a*x**b, get integrand fac*t**rho*g
        fac_ = fac * C * x**(1 + c) / b
        rho = (c + 1)/b

        # we now use t**rho*G(params, t) = G(params + rho, t)
        # [L, page 150, equation (4)]
        # and integral G(params, t) dt = G(1, params+1, 0, t)
        #   (or a similar expression with 1 and 0 exchanged ... pick the one
        #    which yields a well-defined function)
        # [R, section 5]
        # (Note that this dummy will immediately go away again, so we
        #  can safely pass S.One for ``expr``.)
        t = _dummy('t', 'meijerint-indefinite', S.One)

        def tr(p):
            return [a + rho for a in p]
        if any(b.is_integer and (b <= 0) == True for b in tr(g.bm)):
            r = -meijerg(
                list(g.an), list(g.aother) + [1-rho], list(g.bm) + [-rho], list(g.bother), t)
        else:
            r = meijerg(
                list(g.an) + [1-rho], list(g.aother), list(g.bm), list(g.bother) + [-rho], t)
        # The antiderivative is most often expected to be defined
        # in the neighborhood of  x = 0.
        if b.is_extended_nonnegative and not f.subs(x, 0).has(S.NaN, S.ComplexInfinity):
            place = 0  # Assume we can expand at zero
        else:
            place = None
        r = hyperexpand(r.subs(t, a*x**b), place=place)

        # now substitute back
        # Note: we really do want the powers of x to combine.
        res += powdenest(fac_*r, polar=True)

    def _clean(res):
        """This multiplies out superfluous powers of x we created, and chops off
        constants:

            >> _clean(x*(exp(x)/x - 1/x) + 3)
            exp(x)

        cancel is used before mul_expand since it is possible for an
        expression to have an additive constant that does not become isolated
        with simple expansion. Such a situation was identified in issue 6369:

        Examples
        ========

        >>> from sympy import sqrt, cancel
        >>> from sympy.abc import x
        >>> a = sqrt(2*x + 1)
        >>> bad = (3*x*a**5 + 2*x - a**5 + 1)/a**2
        >>> bad.expand().as_independent(x)[0]
        0
        >>> cancel(bad).expand().as_independent(x)[0]
        1
        """
        res = expand_mul(cancel(res), deep=False)
        return Add._from_args(res.as_coeff_add(x)[1])

    res = piecewise_fold(res, evaluate=None)
    if res.is_Piecewise:
        newargs = []
        for e, c in res.args:
            e = _my_unpolarify(_clean(e))
            newargs += [(e, c)]
        res = Piecewise(*newargs, evaluate=False)
    else:
        res = _my_unpolarify(_clean(res))
    return Piecewise((res, _my_unpolarify(cond)), (Integral(f, x), True))

