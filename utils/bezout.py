
def bezout(p, q, x, method='bz'):
    """
    The input polynomials p, q are in Z[x] or in Q[x]. Let
    mx = max(degree(p, x), degree(q, x)).

    The default option bezout(p, q, x, method='bz') returns Bezout's
    symmetric matrix of p and q, of dimensions (mx) x (mx). The
    determinant of this matrix is equal to the determinant of sylvester2,
    Sylvester's matrix of 1853, whose dimensions are (2*mx) x (2*mx);
    however the subresultants of these two matrices may differ.

    The other option, bezout(p, q, x, 'prs'), is of interest to us
    in this module because it returns a matrix equivalent to sylvester2.
    In this case all subresultants of the two matrices are identical.

    Both the subresultant polynomial remainder sequence (prs) and
    the modified subresultant prs of p and q can be computed by
    evaluating determinants of appropriately selected submatrices of
    bezout(p, q, x, 'prs') --- one determinant per coefficient of the
    remainder polynomials.

    The matrices bezout(p, q, x, 'bz') and bezout(p, q, x, 'prs')
    are related by the formula

    bezout(p, q, x, 'prs') =
    backward_eye(deg(p)) * bezout(p, q, x, 'bz') * backward_eye(deg(p)),

    where backward_eye() is the backward identity function.

    References
    ==========
    1. G.M.Diaz-Toca,L.Gonzalez-Vega: Various New Expressions for Subresultants
    and Their Applications. Appl. Algebra in Engin., Communic. and Comp.,
    Vol. 15, 233-266, 2004.

    """
    # obtain degrees of polys
    m, n = degree( Poly(p, x), x), degree( Poly(q, x), x)

    # Special cases:
    # A:: case m = n < 0 (i.e. both polys are 0)
    if m == n and n < 0:
        return Matrix([])

    # B:: case m = n = 0  (i.e. both polys are constants)
    if m == n and n == 0:
        return Matrix([])

    # C:: m == 0 and n < 0 or m < 0 and n == 0
    # (i.e. one poly is constant and the other is 0)
    if m == 0 and n < 0:
        return Matrix([])
    elif m < 0 and n == 0:
        return Matrix([])

    # D:: m >= 1 and n < 0 or m < 0 and n >=1
    # (i.e. one poly is of degree >=1 and the other is 0)
    if m >= 1 and n < 0:
        return Matrix([0])
    elif m < 0 and n >= 1:
        return Matrix([0])

    y = var('y')

    # expr is 0 when x = y
    expr = p * q.subs({x:y}) - p.subs({x:y}) * q

    # hence expr is exactly divisible by x - y
    poly = Poly( quo(expr, x-y), x, y)

    # form Bezout matrix and store them in B as indicated to get
    # the LC coefficient of each poly either in the first position
    # of each row (method='prs') or in the last (method='bz').
    mx = max(m, n)
    B = zeros(mx)
    for i in range(mx):
        for j in range(mx):
            if method == 'prs':
                B[mx - 1 - i, mx - 1 - j] = poly.nth(i, j)
            else:
                B[i, j] = poly.nth(i, j)
    return B

