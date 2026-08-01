
def integrate_hyperexponential_polynomial(p, DE, z):
    """
    Integration of hyperexponential polynomials.

    Explanation
    ===========

    Given a hyperexponential monomial t over k and ``p`` in k[t, 1/t], return q in
    k[t, 1/t] and a bool b in {True, False} such that p - Dq in k if b is True,
    or p - Dq does not have an elementary integral over k(t) if b is False.
    """
    t1 = DE.t
    dtt = DE.d.exquo(Poly(DE.t, DE.t))
    qa = Poly(0, DE.t)
    qd = Poly(1, DE.t)
    b = True

    if p.is_zero:
        return(qa, qd, b)

    from sympy.integrals.rde import rischDE

    with DecrementLevel(DE):
        for i in range(-p.degree(z), p.degree(t1) + 1):
            if not i:
                continue
            elif i < 0:
                # If you get AttributeError: 'NoneType' object has no attribute 'nth'
                # then this should really not have expand=False
                # But it shouldn't happen because p is already a Poly in t and z
                a = p.as_poly(z, expand=False).nth(-i)
            else:
                # If you get AttributeError: 'NoneType' object has no attribute 'nth'
                # then this should really not have expand=False
                a = p.as_poly(t1, expand=False).nth(i)

            aa, ad = frac_in(a, DE.t, field=True)
            aa, ad = aa.cancel(ad, include=True)
            iDt = Poly(i, t1)*dtt
            iDta, iDtd = frac_in(iDt, DE.t, field=True)
            try:
                va, vd = rischDE(iDta, iDtd, Poly(aa, DE.t), Poly(ad, DE.t), DE)
                va, vd = frac_in((va, vd), t1, cancel=True)
            except NonElementaryIntegralException:
                b = False
            else:
                qa = qa*vd + va*Poly(t1**i)*qd
                qd *= vd

    return (qa, qd, b)

