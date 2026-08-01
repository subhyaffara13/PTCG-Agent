
def recognize_derivative(a, d, DE, z=None):
    """
    Compute the squarefree factorization of the denominator of f
    and for each Di the polynomial H in K[x] (see Theorem 2.7.1), using the
    LaurentSeries algorithm. Write Di = GiEi where Gj = gcd(Hn, Di) and
    gcd(Ei,Hn) = 1. Since the residues of f at the roots of Gj are all 0, and
    the residue of f at a root alpha of Ei is Hi(a) != 0, f is the derivative of a
    rational function if and only if Ei = 1 for each i, which is equivalent to
    Di | H[-1] for each i.
    """
    flag =True
    a, d = a.cancel(d, include=True)
    _, r = a.div(d)
    Np, Sp = splitfactor_sqf(d, DE, coefficientD=True, z=z)

    j = 1
    for s, _ in Sp:
        delta_a, delta_d, H = laurent_series(r, d, s, j, DE)
        g = gcd(d, H[-1]).as_poly()
        if g is not d:
            flag = False
            break
        j = j + 1
    return flag

