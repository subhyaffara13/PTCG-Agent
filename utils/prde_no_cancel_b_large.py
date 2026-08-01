
def prde_no_cancel_b_large(b, Q, n, DE):
    """
    Parametric Poly Risch Differential Equation - No cancellation: deg(b) large enough.

    Explanation
    ===========

    Given a derivation D on k[t], n in ZZ, and b, q1, ..., qm in k[t] with
    b != 0 and either D == d/dt or deg(b) > max(0, deg(D) - 1), returns
    h1, ..., hr in k[t] and a matrix A with coefficients in Const(k) such that
    if c1, ..., cm in Const(k) and q in k[t] satisfy deg(q) <= n and
    Dq + b*q == Sum(ci*qi, (i, 1, m)), then q = Sum(dj*hj, (j, 1, r)), where
    d1, ..., dr in Const(k) and A*Matrix([[c1, ..., cm, d1, ..., dr]]).T == 0.
    """
    db = b.degree(DE.t)
    m = len(Q)
    H = [Poly(0, DE.t)]*m

    for N, i in itertools.product(range(n, -1, -1), range(m)):  # [n, ..., 0]
        si = Q[i].nth(N + db)/b.LC()
        sitn = Poly(si*DE.t**N, DE.t)
        H[i] = H[i] + sitn
        Q[i] = Q[i] - derivation(sitn, DE) - b*sitn

    if all(qi.is_zero for qi in Q):
        dc = -1
    else:
        dc = max(qi.degree(DE.t) for qi in Q)
    M = Matrix(dc + 1, m, lambda i, j: Q[j].nth(i), DE.t)
    A, u = constant_system(M, zeros(dc + 1, 1, DE.t), DE)
    c = eye(m, DE.t)
    A = A.row_join(zeros(A.rows, m, DE.t)).col_join(c.row_join(-c))

    return (H, A)

