from typing import Union

def _invert_trig_hyp_real(f, g_ys, symbol):
    """Helper function for inverting trigonometric and hyperbolic functions.

    This helper only handles inversion over the reals.

    For trigonometric functions only finite `g_ys` sets are implemented.

    For hyperbolic functions the set `g_ys` is checked against the domain of the
    respective inverse functions. Infinite `g_ys` sets are also supported.
    """

    if isinstance(f, HyperbolicFunction):
        n = Dummy('n', real=True)

        if isinstance(f, sinh):
            # asinh is defined over R.
            return _invert_real(f.args[0], imageset(n, asinh(n), g_ys), symbol)

        if isinstance(f, cosh):
            g_ys_dom = g_ys.intersect(Interval(1, oo))
            if isinstance(g_ys_dom, Intersection):
                # could not properly resolve domain check
                if isinstance(g_ys, FiniteSet):
                    # If g_ys is a `FiniteSet`` it should be sufficient to just
                    # let the calling `_invert_real()` add an intersection with
                    # `S.Reals` (or a subset `domain`) to ensure that only valid
                    # (real) solutions are returned.
                    # This avoids adding "too many" Intersections or
                    # ConditionSets in the returned set.
                    g_ys_dom = g_ys
                else:
                    return (f, g_ys)
            return _invert_real(f.args[0], Union(
                imageset(n, acosh(n), g_ys_dom),
                imageset(n, -acosh(n), g_ys_dom)), symbol)

        if isinstance(f, sech):
            g_ys_dom = g_ys.intersect(Interval.Lopen(0, 1))
            if isinstance(g_ys_dom, Intersection):
                if isinstance(g_ys, FiniteSet):
                    g_ys_dom = g_ys
                else:
                    return (f, g_ys)
            return _invert_real(f.args[0], Union(
                imageset(n, asech(n), g_ys_dom),
                imageset(n, -asech(n), g_ys_dom)), symbol)

        if isinstance(f, tanh):
            g_ys_dom = g_ys.intersect(Interval.open(-1, 1))
            if isinstance(g_ys_dom, Intersection):
                if isinstance(g_ys, FiniteSet):
                    g_ys_dom = g_ys
                else:
                    return (f, g_ys)
            return _invert_real(f.args[0],
                imageset(n, atanh(n), g_ys_dom), symbol)

        if isinstance(f, coth):
            g_ys_dom = g_ys - Interval(-1, 1)
            if isinstance(g_ys_dom, Complement):
                if isinstance(g_ys, FiniteSet):
                    g_ys_dom = g_ys
                else:
                    return (f, g_ys)
            return _invert_real(f.args[0],
                imageset(n, acoth(n), g_ys_dom), symbol)

        if isinstance(f, csch):
            g_ys_dom = g_ys - FiniteSet(0)
            if isinstance(g_ys_dom, Complement):
                if isinstance(g_ys, FiniteSet):
                    g_ys_dom = g_ys
                else:
                    return (f, g_ys)
            return _invert_real(f.args[0],
                imageset(n, acsch(n), g_ys_dom), symbol)

    elif isinstance(f, TrigonometricFunction) and isinstance(g_ys, FiniteSet):
        def _get_trig_inverses(func):
            global _trig_inverses
            if _trig_inverses is None:
                _trig_inverses = {
                    sin : ((asin, lambda y: pi-asin(y)), 2*pi, Interval(-1, 1)),
                    cos : ((acos, lambda y: -acos(y)), 2*pi, Interval(-1, 1)),
                    tan : ((atan,), pi, S.Reals),
                    cot : ((acot,), pi, S.Reals),
                    sec : ((asec, lambda y: -asec(y)), 2*pi,
                        Union(Interval(-oo, -1), Interval(1, oo))),
                    csc : ((acsc, lambda y: pi-acsc(y)), 2*pi,
                        Union(Interval(-oo, -1), Interval(1, oo)))}
            return _trig_inverses[func]

        invs, period, rng = _get_trig_inverses(f.func)
        n = Dummy('n', integer=True)
        def create_return_set(g):
            # returns ConditionSet that will be part of the final (x, set) tuple
            invsimg = Union(*[
                imageset(n, period*n + inv(g), S.Integers) for inv in invs])
            inv_f, inv_g_ys = _invert_real(f.args[0], invsimg, symbol)
            if inv_f == symbol:     # inversion successful
                conds = rng.contains(g)
                return ConditionSet(symbol, conds, inv_g_ys)
            else:
                return ConditionSet(symbol, Eq(f, g), S.Reals)

        retset = Union(*[create_return_set(g) for g in g_ys])
        return (symbol, retset)

    else:
        return (f, g_ys)

