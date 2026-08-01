
def riemann_cyclic_replace(t_r):
    """
    replace Riemann tensor with an equivalent expression

    ``R(m,n,p,q) -> 2/3*R(m,n,p,q) - 1/3*R(m,q,n,p) + 1/3*R(m,p,n,q)``

    """
    free = sorted(t_r.free, key=lambda x: x[1])
    m, n, p, q = [x[0] for x in free]
    t0 = t_r*Rational(2, 3)
    t1 = -t_r.substitute_indices((m,m),(n,q),(p,n),(q,p))*Rational(1, 3)
    t2 = t_r.substitute_indices((m,m),(n,p),(p,n),(q,q))*Rational(1, 3)
    t3 = t0 + t1 + t2
    return t3

