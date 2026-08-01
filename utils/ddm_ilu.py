
def ddm_ilu(a):
    """a  <--  LU(a)

    Computes the LU decomposition of a matrix in place. Returns a list of
    row swaps that were performed.

    Uses division in the ground domain which should be an exact field.

    This is only suitable for domains like :ref:`GF(p)`, :ref:`QQ`, :ref:`QQ_I`
    and :ref:`QQ(a)`. With a rational function field like :ref:`K(x)` it is
    better to clear denominators and use division-free algorithms. Pivoting is
    used to avoid exact zeros but not for floating point accuracy so :ref:`RR`
    and :ref:`CC` are not suitable (use :func:`ddm_irref` instead).

    Examples
    ========

    >>> from sympy.polys.matrices.dense import ddm_ilu
    >>> from sympy import QQ
    >>> a = [[QQ(1, 2), QQ(1, 3)], [QQ(1, 4), QQ(1, 5)]]
    >>> swaps = ddm_ilu(a)
    >>> swaps
    []
    >>> a
    [[1/2, 1/3], [1/2, 1/30]]

    The same example using ``Matrix``:

    >>> from sympy import Matrix, S
    >>> M = Matrix([[S(1)/2, S(1)/3], [S(1)/4, S(1)/5]])
    >>> L, U, swaps = M.LUdecomposition()
    >>> L
    Matrix([
    [  1, 0],
    [1/2, 1]])
    >>> U
    Matrix([
    [1/2,  1/3],
    [  0, 1/30]])
    >>> swaps
    []

    See Also
    ========

    ddm_irref
    ddm_ilu_solve
    sympy.matrices.matrixbase.MatrixBase.LUdecomposition
    """
    m = len(a)
    if not m:
        return []
    n = len(a[0])

    swaps = []

    for i in range(min(m, n)):
        if not a[i][i]:
            for ip in range(i+1, m):
                if a[ip][i]:
                    swaps.append((i, ip))
                    a[i], a[ip] = a[ip], a[i]
                    break
            else:
                # M = Matrix([[1, 0, 0, 0], [0, 0, 0, 0], [0, 0, 1, 1], [0, 0, 1, 2]])
                continue
        for j in range(i+1, m):
            l_ji = a[j][i] / a[i][i]
            a[j][i] = l_ji
            for k in range(i+1, n):
                a[j][k] -= l_ji * a[i][k]

    return swaps

