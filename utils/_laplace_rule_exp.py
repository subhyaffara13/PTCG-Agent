import re

def _laplace_rule_exp(f, t, s):
    """
    If this function finds a factor ``exp(a*t)``, it applies the
    frequency-shift rule of the Laplace transform and adjusts the convergence
    plane accordingly.  For example, if it gets ``(exp(-a*t)*f(t), t, s)``, it
    will compute ``LaplaceTransform(f(t), t, s+a)``.
    """

    a = Wild('a', exclude=[t])
    y = Wild('y')
    z = Wild('z')
    ma1 = f.match(exp(y)*z)
    if ma1:
        ma2 = ma1[y].collect(t).match(a*t)
        if ma2:
            _debug('     rule: multiply with exp (4.1.5)')
            r, pr, cr = _laplace_transform(ma1[z], t, s-ma2[a],
                                           simplify=False)
            return (r, pr+re(ma2[a]), cr)
    return None

