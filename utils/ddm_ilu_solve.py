
def ddm_ilu_solve(x, L, U, swaps, b):
    """x  <--  solve(L*U*x = swaps(b))

    Solve a linear system, $A*x = b$, given an LU factorization of $A$.

    Uses division in the ground domain which must be a field.

    Modifies $x$ in place.

    Examples
    ========

    Compute the LU decomposition of $A$ (in place):

    >>> from sympy import QQ
    >>> from sympy.polys.matrices.dense import ddm_ilu, ddm_ilu_solve
    >>> A = [[QQ(1), QQ(2)], [QQ(3), QQ(4)]]
    >>> swaps = ddm_ilu(A)
    >>> A
    [[1, 2], [3, -2]]
    >>> L = U = A

    Solve the linear system:

    >>> b = [[QQ(5)], [QQ(6)]]
    >>> x = [[None], [None]]
    >>> ddm_ilu_solve(x, L, U, swaps, b)
    >>> x
    [[-4], [9/2]]

    See Also
    ========

    ddm_ilu
        Compute the LU decomposition of a matrix in place.
    ddm_ilu_split
        Compute the LU decomposition of a matrix and separate $L$ and $U$.
    sympy.polys.matrices.domainmatrix.DomainMatrix.lu_solve
        Higher level interface to this function.
    """
    m = len(U)
    if not m:
        return
    n = len(U[0])

    m2 = len(b)
    if not m2:
        raise DMShapeError("Shape mismtch")
    o = len(b[0])

    if m != m2:
        raise DMShapeError("Shape mismtch")
    if m < n:
        raise NotImplementedError("Underdetermined")

    if swaps:
        b = [row[:] for row in b]
        for i1, i2 in swaps:
            b[i1], b[i2] = b[i2], b[i1]

    # solve Ly = b
    y = [[None] * o for _ in range(m)]
    for k in range(o):
        for i in range(m):
            rhs = b[i][k]
            for j in range(i):
                rhs -= L[i][j] * y[j][k]
            y[i][k] = rhs

    if m > n:
        for i in range(n, m):
            for j in range(o):
                if y[i][j]:
                    raise DMNonInvertibleMatrixError

    # Solve Ux = y
    for k in range(o):
        for i in reversed(range(n)):
            if not U[i][i]:
                raise DMNonInvertibleMatrixError
            rhs = y[i][k]
            for j in range(i+1, n):
                rhs -= U[i][j] * x[j][k]
            x[i][k] = rhs / U[i][i]

