
def heuristics(e, z, z0, dir):
    """Computes the limit of an expression term-wise.
    Parameters are the same as for the ``limit`` function.
    Works with the arguments of expression ``e`` one by one, computing
    the limit of each and then combining the results. This approach
    works only for simple limits, but it is fast.
    """

    rv = None
    if z0 is S.Infinity:
        rv = limit(e.subs(z, 1/z), z, S.Zero, "+")
        if isinstance(rv, Limit):
            return
    elif (e.is_Mul or e.is_Add or e.is_Pow or (e.is_Function and not isinstance(e, AppliedUndef))):
        r = []
        from sympy.simplify.simplify import together
        for a in e.args:
            l = limit(a, z, z0, dir)
            if l.has(S.Infinity) and l.is_finite is None:
                if isinstance(e, Add):
                    m = factor_terms(e)
                    if not isinstance(m, Mul): # try together
                        m = together(m)
                    if not isinstance(m, Mul): # try factor if the previous methods failed
                        m = factor(e)
                    if isinstance(m, Mul):
                        return heuristics(m, z, z0, dir)
                    return
                return
            elif isinstance(l, Limit):
                return
            elif l is S.NaN:
                return
            else:
                r.append(l)
        if r:
            rv = e.func(*r)
            if rv is S.NaN and e.is_Mul and any(isinstance(rr, AccumBounds) for rr in r):
                r2 = []
                e2 = []
                for ii, rval in enumerate(r):
                    if isinstance(rval, AccumBounds):
                        r2.append(rval)
                    else:
                        e2.append(e.args[ii])

                if len(e2) > 0:
                    e3 = Mul(*e2).simplify()
                    l = limit(e3, z, z0, dir)
                    rv = l * Mul(*r2)

            if rv is S.NaN:
                try:
                    from sympy.simplify.ratsimp import ratsimp
                    rat_e = ratsimp(e)
                except PolynomialError:
                    return
                if rat_e is S.NaN or rat_e == e:
                    return
                return limit(rat_e, z, z0, dir)
    return rv

