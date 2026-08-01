
def param_rischDE(fa, fd, G, DE):
    """
    Solve a Parametric Risch Differential Equation: Dy + f*y == Sum(ci*Gi, (i, 1, m)).

    Explanation
    ===========

    Given a derivation D in k(t), f in k(t), and G
    = [G1, ..., Gm] in k(t)^m, return h = [h1, ..., hr] in k(t)^r and
    a matrix A with m + r columns and entries in Const(k) such that
    Dy + f*y = Sum(ci*Gi, (i, 1, m)) has a solution y
    in k(t) with c1, ..., cm in Const(k) if and only if y = Sum(dj*hj,
    (j, 1, r)) where d1, ..., dr are in Const(k) and (c1, ..., cm,
    d1, ..., dr) is a solution of Ax == 0.

    Elements of k(t) are tuples (a, d) with a and d in k[t].
    """
    m = len(G)
    q, (fa, fd) = weak_normalizer(fa, fd, DE)
    # Solutions of the weakly normalized equation Dz + f*z = q*Sum(ci*Gi)
    # correspond to solutions y = z/q of the original equation.
    gamma = q
    G = [(q*ga).cancel(gd, include=True) for ga, gd in G]

    a, (ba, bd), G, hn = prde_normal_denom(fa, fd, G, DE)
    # Solutions q in k<t> of  a*Dq + b*q = Sum(ci*Gi) correspond
    # to solutions z = q/hn of the weakly normalized equation.
    gamma *= hn

    A, B, G, hs = prde_special_denom(a, ba, bd, G, DE)
    # Solutions p in k[t] of  A*Dp + B*p = Sum(ci*Gi) correspond
    # to solutions q = p/hs of the previous equation.
    gamma *= hs

    g = A.gcd(B)
    a, b, g = A.quo(g), B.quo(g), [gia.cancel(gid*g, include=True) for
        gia, gid in G]

    # a*Dp + b*p = Sum(ci*gi)  may have a polynomial solution
    # only if the sum is in k[t].

    q, M = prde_linear_constraints(a, b, g, DE)

    # q = [q1, ..., qm] where qi in k[t] is the polynomial component
    # of the partial fraction expansion of gi.
    # M is a matrix with m columns and entries in k.
    # Sum(fi*gi, (i, 1, m)), where f1, ..., fm are elements of k,
    # is a polynomial if and only if M*Matrix([f1, ..., fm]) == 0,
    # in which case the sum is equal to Sum(fi*qi).

    M, _ = constant_system(M, zeros(M.rows, 1, DE.t), DE)
    # M is a matrix with m columns and entries in Const(k).
    # Sum(ci*gi) is in k[t] for c1, ..., cm in Const(k)
    # if and only if M*Matrix([c1, ..., cm]) == 0,
    # in which case the sum is Sum(ci*qi).

    ## Reduce number of constants at this point

    V = M.nullspace()
    # V = [v1, ..., vu] where each vj is a column matrix with
    # entries aj1, ..., ajm in Const(k).
    # Sum(aji*gi) is in k[t] and equal to Sum(aji*qi) (j = 1, ..., u).
    # Sum(ci*gi) is in k[t] if and only is ci = Sum(dj*aji)
    # (i = 1, ..., m) for some d1, ..., du in Const(k).
    # In that case,
    #     Sum(ci*gi) = Sum(ci*qi) = Sum(dj*Sum(aji*qi)) = Sum(dj*rj)
    # where rj = Sum(aji*qi) (j = 1, ..., u) in k[t].

    if not V:  # No non-trivial solution
        return [], eye(m, DE.t)

    Mq = Matrix([q])  # A single row.
    r = [(Mq*vj)[0] for vj in V]  # [r1, ..., ru]

    # Solutions of a*Dp + b*p = Sum(dj*rj) correspond to solutions
    # y = p/gamma of the initial equation with ci = Sum(dj*aji).

    try:
        # We try n=5. At least for prde_spde, it will always
        # terminate no matter what n is.
        n = bound_degree(a, b, r, DE, parametric=True)
    except NotImplementedError:
        # A temporary bound is set. Eventually, it will be removed.
        # the currently added test case takes large time
        # even with n=5, and much longer with large n's.
        n = 5

    h, B = param_poly_rischDE(a, b, r, n, DE)

    # h = [h1, ..., hv] in k[t]^v and and B is a matrix with u + v
    # columns and entries in Const(k) such that
    # a*Dp + b*p = Sum(dj*rj) has a solution p of degree <= n
    # in k[t] if and only if p = Sum(ek*hk) where e1, ..., ev are in
    # Const(k) and B*Matrix([d1, ..., du, e1, ..., ev]) == 0.
    # The solutions of the original equation for ci = Sum(dj*aji)
    # (i = 1, ..., m) are then y = Sum(ek*hk, (k, 1, v))/gamma.

    ## Build combined relation matrix with m + u + v columns.

    A = -eye(m, DE.t)
    for vj in V:
        A = A.row_join(vj)
    A = A.row_join(zeros(m, len(h), DE.t))
    A = A.col_join(zeros(B.rows, m, DE.t).row_join(B))

    ## Eliminate d1, ..., du.

    W = A.nullspace()

    # W = [w1, ..., wt] where each wl is a column matrix with
    # entries blk (k = 1, ..., m + u + v) in Const(k).
    # The vectors (bl1, ..., blm) generate the space of those
    # constant families (c1, ..., cm) for which a solution of
    # the equation Dy + f*y == Sum(ci*Gi) exists. They generate
    # the space and form a basis except possibly when Dy + f*y == 0
    # is solvable in k(t}. The corresponding solutions are
    # y = Sum(blk'*hk, (k, 1, v))/gamma, where k' = k + m + u.

    v = len(h)
    shape = (len(W), m+v)
    elements = [wl[:m] + wl[-v:] for wl in W] # excise dj's.
    items = [e for row in elements for e in row]

    # Need to set the shape in case W is empty
    M = Matrix(*shape, items, DE.t)
    N = M.nullspace()

    # N = [n1, ..., ns] where the ni in Const(k)^(m + v) are column
    # vectors generating the space of linear relations between
    # c1, ..., cm, e1, ..., ev.

    C = Matrix([ni[:] for ni in N], DE.t)  # rows n1, ..., ns.

    return [hk.cancel(gamma, include=True) for hk in h], C

