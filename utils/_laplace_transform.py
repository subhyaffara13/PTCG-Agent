
def _laplace_transform(fn, t_, s_, *, simplify):
    """
    Front-end function of the Laplace transform. It tries to apply all known
    rules recursively, and if everything else fails, it tries to integrate.
    """

    terms_t = Add.make_args(fn)
    terms_s = []
    terms = []
    planes = []
    conditions = []

    for ff in terms_t:
        k, ft = ff.as_independent(t_, as_Add=False)
        if ft.has(SingularityFunction):
            _terms = Add.make_args(ft.rewrite(Heaviside))
            for _term in _terms:
                k1, f1 = _term.as_independent(t_, as_Add=False)
                terms.append((k*k1, f1))
        elif ft.func == Piecewise and not ft.has(DiracDelta(t_)):
            _terms = Add.make_args(_piecewise_to_heaviside(ft, t_))
            for _term in _terms:
                k1, f1 = _term.as_independent(t_, as_Add=False)
                terms.append((k*k1, f1))
        else:
            terms.append((k, ft))

    for k, ft in terms:
        if ft.has(SingularityFunction):
            r = (LaplaceTransform(ft, t_, s_), S.NegativeInfinity, True)
        else:
            if ft.has(Heaviside(t_)) and not ft.has(DiracDelta(t_)):
                # For t>=0, Heaviside(t)=1 can be used, except if there is also
                # a DiracDelta(t) present, in which case removing Heaviside(t)
                # is unnecessary because _laplace_rule_delta can deal with it.
                ft = ft.subs(Heaviside(t_), 1)
            if (
                    (r := _laplace_apply_simple_rules(ft, t_, s_))
                    is not None or
                    (r := _laplace_apply_prog_rules(ft, t_, s_))
                    is not None or
                    (r := _laplace_expand(ft, t_, s_)) is not None):
                pass
            elif any(undef.has(t_) for undef in ft.atoms(AppliedUndef)):
                # If there are undefined functions f(t) then integration is
                # unlikely to do anything useful so we skip it and given an
                # unevaluated LaplaceTransform.
                r = (LaplaceTransform(ft, t_, s_), S.NegativeInfinity, True)
            elif (r := _laplace_transform_integration(
                    ft, t_, s_, simplify=simplify)) is not None:
                pass
            else:
                r = (LaplaceTransform(ft, t_, s_), S.NegativeInfinity, True)
        (ri_, pi_, ci_) = r
        terms_s.append(k*ri_)
        planes.append(pi_)
        conditions.append(ci_)

    result = Add(*terms_s)
    if simplify:
        result = result.simplify(doit=False)
    plane = Max(*planes)
    condition = And(*conditions)

    return result, plane, condition

