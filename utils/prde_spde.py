
def prde_spde(a, b, Q, n, DE):
    """
    Special Polynomial Differential Equation algorithm: Parametric Version.

    Explanation
    ===========

    Given a derivation D on k[t], an integer n, and a, b, q1, ..., qm in k[t]
    with deg(a) > 0 and gcd(a, b) == 1, return (A, B, Q, R, n1), with
    Qq = [q1, ..., qm] and R = [r1, ..., rm], such that for any solution
    c1, ..., cm in Const(k) and q in k[t] of degree at most n of
    a*Dq + b*q == Sum(ci*gi, (i, 1, m)), p = (q - Sum(ci*ri, (i, 1, m)))/a has
    degree at most n1 and satisfies A*Dp + B*p == Sum(ci*qi, (i, 1, m))
    """
    R, Z = list(zip(*[gcdex_diophantine(b, a, qi) for qi in Q]))

    A = a
    B = b + derivation(a, DE)
    Qq = [zi - derivation(ri, DE) for ri, zi in zip(R, Z)]
    R = list(R)
    n1 = n - a.degree(DE.t)

    return (A, B, Qq, R, n1)

