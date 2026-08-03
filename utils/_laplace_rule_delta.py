import re

def _laplace_rule_delta(f, t, s):
    """
    If this function finds a factor ``DiracDelta(b*t-a)``, it applies the
    masking property of the delta distribution. For example, if it gets
    ``(DiracDelta(t-a)*f(t), t, s)``, it will return
    ``(f(a)*exp(-a*s), -a, True)``.
    """
    # This rule is not in Bateman54

    a = Wild('a', exclude=[t])
    b = Wild('b', exclude=[t])

    y = Wild('y')
    z = Wild('z')
    ma1 = f.match(DiracDelta(y)*z)
    if ma1 and not ma1[z].has(DiracDelta):
        ma2 = ma1[y].collect(t).match(b*t-a)
        if ma2:
            _debug('     rule: multiply with DiracDelta')
            loc = ma2[a]/ma2[b]
            if re(loc) >= 0 and im(loc) == 0:
                fn = exp(-ma2[a]/ma2[b]*s)*ma1[z]
                if fn.has(sin, cos):
                    # Then it may be possible that a sinc() is present in the
                    # term; let's try this:
                    fn = fn.rewrite(sinc).ratsimp()
                n, d = [x.subs(t, ma2[a]/ma2[b]) for x in fn.as_numer_denom()]
                if d != 0:
                    return (n/d/ma2[b], S.NegativeInfinity, S.true)
                else:
                    return None
            else:
                return (0, S.NegativeInfinity, S.true)
        if ma1[y].is_polynomial(t):
            ro = roots(ma1[y], t)
            if ro != {} and set(ro.values()) == {1}:
                slope = diff(ma1[y], t)
                r = Add(
                    *[exp(-x*s)*ma1[z].subs(t, s)/slope.subs(t, x)
                      for x in list(ro.keys()) if im(x) == 0 and re(x) >= 0])
                return (r, S.NegativeInfinity, S.true)
    return None

