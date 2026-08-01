
def _inverse_laplace_apply_simple_rules(f, s, t):
    """
    Helper function for the class InverseLaplaceTransform.
    """
    if f == 1:
        _debug('     rule: 1 o---o DiracDelta()')
        return DiracDelta(t), S.true

    _ILT_rules, s_, t_ = _inverse_laplace_build_rules()
    _prep = ''
    fsubs = f.subs({s: s_})

    for s_dom, t_dom, check, prep, fac in _ILT_rules:
        if _prep != (prep, fac):
            _F = prep(fsubs*fac)
            _prep = (prep, fac)
        ma = _F.match(s_dom)
        if ma:
            c = check
            if c is not S.true:
                args = [x.xreplace(ma) for x in c[0]]
                c = c[1](*args)
            if c == S.true:
                return Heaviside(t)*t_dom.xreplace(ma).subs({t_: t}), S.true

    return None

