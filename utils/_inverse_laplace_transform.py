
def _inverse_laplace_transform(fn, s_, t_, plane, *, simplify, dorational):
    """
    Front-end function of the inverse Laplace transform. It tries to apply all
    known rules recursively.  If everything else fails, it tries to integrate.
    """
    terms = Add.make_args(fn)
    terms_t = []
    conditions = []

    for term in terms:
        if term.has(exp):
            # Simplify expressions with exp() such that time-shifted
            # expressions have negative exponents in the numerator instead of
            # positive exponents in the numerator and denominator; this is a
            # (necessary) trick. It will, for example, convert
            # (s**2*exp(2*s) + 4*exp(s) - 4)*exp(-2*s)/(s*(s**2 + 1)) into
            # (s**2 + 4*exp(-s) - 4*exp(-2*s))/(s*(s**2 + 1))
            term = term.subs(s_, -s_).together().subs(s_, -s_)
        k, f = term.as_independent(s_, as_Add=False)
        if (
                dorational and term.is_rational_function(s_) and
                (r := _inverse_laplace_rational(
                    f, s_, t_, plane, simplify=simplify))
                is not None or
                (r := _inverse_laplace_apply_simple_rules(f, s_, t_))
                is not None or
                (r := _inverse_laplace_early_prog_rules(f, s_, t_, plane))
                is not None or
                (r := _inverse_laplace_expand(f, s_, t_, plane))
                is not None or
                (r := _inverse_laplace_apply_prog_rules(f, s_, t_, plane))
                is not None):
            pass
        elif any(undef.has(s_) for undef in f.atoms(AppliedUndef)):
            # If there are undefined functions f(t) then integration is
            # unlikely to do anything useful so we skip it and given an
            # unevaluated LaplaceTransform.
            r = (InverseLaplaceTransform(f, s_, t_, plane), S.true)
        elif (
                r := _inverse_laplace_transform_integration(
                    f, s_, t_, plane, simplify=simplify)) is not None:
            pass
        else:
            r = (InverseLaplaceTransform(f, s_, t_, plane), S.true)
        (ri_, ci_) = r
        terms_t.append(k*ri_)
        conditions.append(ci_)

    result = Add(*terms_t)
    if simplify:
        result = result.simplify(doit=False)
    condition = And(*conditions)

    return result, condition

