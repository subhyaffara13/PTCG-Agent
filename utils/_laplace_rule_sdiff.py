
def _laplace_rule_sdiff(f, t, s):
    """
    This function looks for multiplications with polynoimials in `t` as they
    correspond to differentiation in the frequency domain. For example, if it
    gets ``(t*f(t), t, s)``, it will compute
    ``-Derivative(LaplaceTransform(f(t), t, s), s)``.
    """

    if f.is_Mul:
        pfac = [1]
        ofac = [1]
        for fac in Mul.make_args(f):
            if fac.is_polynomial(t):
                pfac.append(fac)
            else:
                ofac.append(fac)
        if len(pfac) > 1:
            pex = prod(pfac)
            pc = Poly(pex, t).all_coeffs()
            N = len(pc)
            if N > 1:
                oex = prod(ofac)
                r_, p_, c_ = _laplace_transform(oex, t, s, simplify=False)
                deri = [r_]
                d1 = False
                try:
                    d1 = -diff(deri[-1], s)
                except ValueError:
                    d1 = False
                if r_.has(LaplaceTransform):
                    for k in range(N-1):
                        deri.append((-1)**(k+1)*Derivative(r_, s, k+1))
                elif d1:
                    deri.append(d1)
                    for k in range(N-2):
                        deri.append(-diff(deri[-1], s))
                if d1:
                    r = Add(*[pc[N-n-1]*deri[n] for n in range(N)])
                    return (r, p_, c_)
    # We still have to cover the possibility that there is a symbolic positive
    # integer exponent.
    n = Wild('n', exclude=[t])
    g = Wild('g')
    if ma1 := f.match(t**n*g):
        if ma1[n].is_integer and ma1[n].is_positive:
            r_, p_, c_ = _laplace_transform(ma1[g], t, s, simplify=False)
            return (-1)**ma1[n]*diff(r_, (s, ma1[n])), p_, c_
    return None

