
def _laplace_rule_diff(f, t, s):
    """
    This function looks for derivatives in the time domain and replaces it
    by factors of `s` and initial conditions in the frequency domain. For
    example, if it gets ``(diff(f(t), t), t, s)``, it will compute
    ``s*LaplaceTransform(f(t), t, s) - f(0)``.
    """

    a = Wild('a', exclude=[t])
    n = Wild('n', exclude=[t])
    g = WildFunction('g')
    ma1 = f.match(a*Derivative(g, (t, n)))
    if ma1 and ma1[n].is_integer:
        m = [z.has(t) for z in ma1[g].args]
        if sum(m) == 1:
            _debug('     rule: time derivative (4.1.8)')
            d = []
            for k in range(ma1[n]):
                if k == 0:
                    y = ma1[g].subs(t, 0)
                else:
                    y = Derivative(ma1[g], (t, k)).subs(t, 0)
                d.append(s**(ma1[n]-k-1)*y)
            r, pr, cr = _laplace_transform(ma1[g], t, s, simplify=False)
            return (ma1[a]*(s**ma1[n]*r - Add(*d)),  pr, cr)
    return None

