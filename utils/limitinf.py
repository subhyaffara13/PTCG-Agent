
def limitinf(e, x):
    """Limit e(x) for x-> oo."""
    # rewrite e in terms of tractable functions only

    old = e
    if not e.has(x):
        return e  # e is a constant
    from sympy.simplify.powsimp import powdenest
    from sympy.calculus.util import AccumBounds
    if e.has(Order):
        e = e.expand().removeO()
    if not x.is_positive or x.is_integer:
        # We make sure that x.is_positive is True and x.is_integer is None
        # so we get all the correct mathematical behavior from the expression.
        # We need a fresh variable.
        p = Dummy('p', positive=True)
        e = e.subs(x, p)
        x = p
    e = e.rewrite('tractable', deep=True, limitvar=x)
    e = powdenest(e)
    if isinstance(e, AccumBounds):
        if mrv_leadterm(e.min, x) != mrv_leadterm(e.max, x):
            raise NotImplementedError
        c0, e0 = mrv_leadterm(e.min, x)
    else:
        c0, e0 = mrv_leadterm(e, x)
    sig = sign(e0, x)
    if sig == 1:
        return S.Zero  # e0>0: lim f = 0
    elif sig == -1:  # e0<0: lim f = +-oo (the sign depends on the sign of c0)
        if c0.match(I*Wild("a", exclude=[I])):
            return c0*oo
        s = sign(c0, x)
        # the leading term shouldn't be 0:
        if s == 0:
            raise ValueError("Leading term should not be 0")
        return s*oo
    elif sig == 0:
        if c0 == old:
            c0 = c0.cancel()
        return limitinf(c0, x)  # e0=0: lim f = lim c0
    else:
        raise ValueError("{} could not be evaluated".format(sig))

