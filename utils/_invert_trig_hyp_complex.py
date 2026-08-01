
def _invert_trig_hyp_complex(f, g_ys, symbol):
    """Helper function for inverting trigonometric and hyperbolic functions.

    This helper only handles inversion over the complex numbers.
    Only finite `g_ys` sets are implemented.

    Handling of singularities is only implemented for hyperbolic equations.
    In case of a symbolic element g in g_ys a ConditionSet may be returned.
    """

    if isinstance(f, TrigonometricFunction) and isinstance(g_ys, FiniteSet):
        def inv(trig):
            if isinstance(trig, (sin, csc)):
                F = asin if isinstance(trig, sin) else acsc
                return (
                    lambda a: 2*n*pi + F(a),
                    lambda a: 2*n*pi + pi - F(a))
            if isinstance(trig, (cos, sec)):
                F = acos if isinstance(trig, cos) else asec
                return (
                    lambda a: 2*n*pi + F(a),
                    lambda a: 2*n*pi - F(a))
            if isinstance(trig, (tan, cot)):
                return (lambda a: n*pi + trig.inverse()(a),)

        n = Dummy('n', integer=True)
        invs = S.EmptySet
        for L in inv(f):
            invs += Union(*[imageset(Lambda(n, L(g)), S.Integers) for g in g_ys])
        return _invert_complex(f.args[0], invs, symbol)

    elif isinstance(f, HyperbolicFunction) and isinstance(g_ys, FiniteSet):
        # There are two main options regarding singularities / domain checking
        # for symbolic elements in g_ys:
        # 1. Add a "catch-all" intersection with S.Complexes.
        # 2. ConditionSets.
        # At present ConditionSets seem to work better and have the additional
        # benefit of representing the precise conditions that must be satisfied.
        # The conditions are also rather straightforward. (At most two isolated
        # points.)
        def _get_hyp_inverses(func):
            global _hyp_inverses
            if _hyp_inverses is None:
                _hyp_inverses = {
                    sinh : ((asinh, lambda y: I*pi-asinh(y)), 2*I*pi, ()),
                    cosh : ((acosh, lambda y: -acosh(y)), 2*I*pi, ()),
                    tanh : ((atanh,), I*pi, (-1, 1)),
                    coth : ((acoth,), I*pi, (-1, 1)),
                    sech : ((asech, lambda y: -asech(y)), 2*I*pi, (0, )),
                    csch : ((acsch, lambda y: I*pi-acsch(y)), 2*I*pi, (0, ))}
            return _hyp_inverses[func]

        # invs: iterable of main inverses, e.g. (acosh, -acosh).
        # excl: iterable of singularities to be checked for.
        invs, period, excl = _get_hyp_inverses(f.func)
        n = Dummy('n', integer=True)
        def create_return_set(g):
            # returns ConditionSet that will be part of the final (x, set) tuple
            invsimg = Union(*[
                imageset(n, period*n + inv(g), S.Integers) for inv in invs])
            inv_f, inv_g_ys = _invert_complex(f.args[0], invsimg, symbol)
            if inv_f == symbol:     # inversion successful
                conds = And(*[Ne(g, e) for e in excl])
                return ConditionSet(symbol, conds, inv_g_ys)
            else:
                return ConditionSet(symbol, Eq(f, g), S.Complexes)

        retset = Union(*[create_return_set(g) for g in g_ys])
        return (symbol, retset)

    else:
        return (f, g_ys)

