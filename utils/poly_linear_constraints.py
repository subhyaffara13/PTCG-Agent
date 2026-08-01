
def poly_linear_constraints(p, d):
    """
    Given p = [p1, ..., pm] in k[t]^m and d in k[t], return
    q = [q1, ..., qm] in k[t]^m and a matrix M with entries in k such
    that Sum(ci*pi, (i, 1, m)), for c1, ..., cm in k, is divisible
    by d if and only if (c1, ..., cm) is a solution of Mx = 0, in
    which case the quotient is Sum(ci*qi, (i, 1, m)).
    """
    m = len(p)
    q, r = zip(*[pi.div(d) for pi in p])

    if not all(ri.is_zero for ri in r):
        n = max(ri.degree() for ri in r)
        M = Matrix(n + 1, m, lambda i, j: r[j].nth(i), d.gens)
    else:
        M = Matrix(0, m, [], d.gens)  # No constraints.

    return q, M

