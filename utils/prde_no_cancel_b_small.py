
def prde_no_cancel_b_small(b, Q, n, DE):
    """
    Parametric Poly Risch Differential Equation - No cancellation: deg(b) small enough.

    Explanation
    ===========

    Given a derivation D on k[t], n in ZZ, and b, q1, ..., qm in k[t] with
    deg(b) < deg(D) - 1 and either D == d/dt or deg(D) >= 2, returns
    h1, ..., hr in k[t] and a matrix A with coefficients in Const(k) such that
    if c1, ..., cm in Const(k) and q in k[t] satisfy deg(q) <= n and
    Dq + b*q == Sum(ci*qi, (i, 1, m)) then q = Sum(dj*hj, (j, 1, r)) where
    d1, ..., dr in Const(k) and A*Matrix([[c1, ..., cm, d1, ..., dr]]).T == 0.
    """
    m = len(Q)
    H = [Poly(0, DE.t)]*m

    for N, i in itertools.product(range(n, 0, -1), range(m)):  # [n, ..., 1]
        si = Q[i].nth(N + DE.d.degree(DE.t) - 1)/(N*DE.d.LC())
        sitn = Poly(si*DE.t**N, DE.t)
        H[i] = H[i] + sitn
        Q[i] = Q[i] - derivation(sitn, DE) - b*sitn

    if b.degree(DE.t) > 0:
        for i in range(m):
            si = Poly(Q[i].nth(b.degree(DE.t))/b.LC(), DE.t)
            H[i] = H[i] + si
            Q[i] = Q[i] - derivation(si, DE) - b*si
        if all(qi.is_zero for qi in Q):
            dc = -1
        else:
            dc = max(qi.degree(DE.t) for qi in Q)
        M = Matrix(dc + 1, m, lambda i, j: Q[j].nth(i), DE.t)
        A, u = constant_system(M, zeros(dc + 1, 1, DE.t), DE)
        c = eye(m, DE.t)
        A = A.row_join(zeros(A.rows, m, DE.t)).col_join(c.row_join(-c))
        return (H, A)

    # else: b is in k, deg(qi) < deg(Dt)

    t = DE.t
    if DE.case != 'base':
        with DecrementLevel(DE):
            t0 = DE.t  # k = k0(t0)
            ba, bd = frac_in(b, t0, field=True)
            Q0 = [frac_in(qi.TC(), t0, field=True) for qi in Q]
            f, B = param_rischDE(ba, bd, Q0, DE)

            # f = [f1, ..., fr] in k^r and B is a matrix with
            # m + r columns and entries in Const(k) = Const(k0)
            # such that Dy0 + b*y0 = Sum(ci*qi, (i, 1, m)) has
            # a solution y0 in k with c1, ..., cm in Const(k)
            # if and only y0 = Sum(dj*fj, (j, 1, r)) where
            # d1, ..., dr ar in Const(k) and
            # B*Matrix([c1, ..., cm, d1, ..., dr]) == 0.

        # Transform fractions (fa, fd) in f into constant
        # polynomials fa/fd in k[t].
        # (Is there a better way?)
        f = [Poly(fa.as_expr()/fd.as_expr(), t, field=True)
             for fa, fd in f]
        B = Matrix.from_Matrix(B.to_Matrix(), t)
    else:
        # Base case. Dy == 0 for all y in k and b == 0.
        # Dy + b*y = Sum(ci*qi) is solvable if and only if
        # Sum(ci*qi) == 0 in which case the solutions are
        # y = d1*f1 for f1 = 1 and any d1 in Const(k) = k.

        f = [Poly(1, t, field=True)]  # r = 1
        B = Matrix([[qi.TC() for qi in Q] + [S.Zero]], DE.t)
        # The condition for solvability is
        # B*Matrix([c1, ..., cm, d1]) == 0
        # There are no constraints on d1.

    # Coefficients of t^j (j > 0) in Sum(ci*qi) must be zero.
    d = max(qi.degree(DE.t) for qi in Q)
    if d > 0:
        M = Matrix(d, m, lambda i, j: Q[j].nth(i + 1), DE.t)
        A, _ = constant_system(M, zeros(d, 1, DE.t), DE)
    else:
        # No constraints on the hj.
        A = Matrix(0, m, [], DE.t)

    # Solutions of the original equation are
    #    y = Sum(dj*fj, (j, 1, r) + Sum(ei*hi, (i, 1, m)),
    # where  ei == ci  (i = 1, ..., m),  when
    # A*Matrix([c1, ..., cm]) == 0 and
    # B*Matrix([c1, ..., cm, d1, ..., dr]) == 0

    # Build combined constraint matrix with m + r + m columns.

    r = len(f)
    I = eye(m, DE.t)
    A = A.row_join(zeros(A.rows, r + m, DE.t))
    B = B.row_join(zeros(B.rows, m, DE.t))
    C = I.row_join(zeros(m, r, DE.t)).row_join(-I)

    return f + H, A.col_join(B).col_join(C)

