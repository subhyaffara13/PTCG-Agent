
def _laplace_apply_simple_rules(f, t, s):
    """
    This function applies all simple rules and returns the result if one
    of them gives a result.
    """
    simple_rules, t_, s_ = _laplace_build_rules()
    prep_old = ''
    prep_f = ''
    for t_dom, s_dom, check, plane, prep in simple_rules:
        if prep_old != prep:
            prep_f = prep(f.subs({t: t_}))
            prep_old = prep
        ma = prep_f.match(t_dom)
        if ma:
            try:
                c = check.xreplace(ma)
            except TypeError:
                # This may happen if the time function has imaginary
                # numbers in it. Then we give up.
                continue
            if c == S.true:
                return (s_dom.xreplace(ma).subs({s_: s}),
                        plane.xreplace(ma), S.true)
    return None

