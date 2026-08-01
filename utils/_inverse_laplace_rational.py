
def _inverse_laplace_rational(fn, s, t, plane, *, simplify):
    """
    Helper function for the class InverseLaplaceTransform.
    """
    x_ = symbols('x_')
    f = fn.apart(s)
    terms = Add.make_args(f)
    terms_t = []
    conditions = [S.true]
    for term in terms:
        [n, d] = term.as_numer_denom()
        dc = d.as_poly(s).all_coeffs()
        dc_lead = dc[0]
        dc = [x/dc_lead for x in dc]
        nc = [x/dc_lead for x in n.as_poly(s).all_coeffs()]
        if len(dc) == 1:
            N = len(nc)-1
            for c in enumerate(nc):
                r = c[1]*DiracDelta(t, N-c[0])
                terms_t.append(r)
        elif len(dc) == 2:
            r = nc[0]*exp(-dc[1]*t)
            terms_t.append(Heaviside(t)*r)
        elif len(dc) == 3:
            a = dc[1]/2
            b = (dc[2]-a**2).factor()
            if len(nc) == 1:
                nc = [S.Zero] + nc
            l, m = tuple(nc)
            if b == 0:
                r = (m*t+l*(1-a*t))*exp(-a*t)
            else:
                hyp = False
                if b.is_negative:
                    b = -b
                    hyp = True
                b2 = list(roots(x_**2-b, x_).keys())[0]
                bs = sqrt(b).simplify()
                if hyp:
                    r = (
                        l*exp(-a*t)*cosh(b2*t) + (m-a*l) /
                        bs*exp(-a*t)*sinh(bs*t))
                else:
                    r = l*exp(-a*t)*cos(b2*t) + (m-a*l)/bs*exp(-a*t)*sin(bs*t)
            terms_t.append(Heaviside(t)*r)
        else:
            ft, cond = _inverse_laplace_transform(
                term, s, t, plane, simplify=simplify, dorational=False)
            terms_t.append(ft)
            conditions.append(cond)

    result = Add(*terms_t)
    if simplify:
        result = result.simplify(doit=False)
    return result, And(*conditions)

