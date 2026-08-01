
def ddm_ilu_split(L, U, K):
    """L, U  <--  LU(U)

    Compute the LU decomposition of a matrix $L$ in place and store the lower
    and upper triangular matrices in $L$ and $U$, respectively. Returns a list
    of row swaps that were performed.

    Uses division in the ground domain which should be an exact field.

    Examples
    ========

    >>> from sympy.polys.matrices.ddm import ddm_ilu_split
    >>> from sympy import QQ
    >>> L = [[QQ(0), QQ(0)], [QQ(0), QQ(0)]]
    >>> U = [[QQ(1), QQ(2)], [QQ(3), QQ(4)]]
    >>> swaps = ddm_ilu_split(L, U, QQ)
    >>> swaps
    []
    >>> L
    [[0, 0], [3, 0]]
    >>> U
    [[1, 2], [0, -2]]

    See Also
    ========

    ddm_ilu
    ddm_ilu_solve
    """
    m = len(U)
    if not m:
        return []
    n = len(U[0])

    swaps = ddm_ilu(U)

    zeros = [K.zero] * min(m, n)
    for i in range(1, m):
        j = min(i, n)
        L[i][:j] = U[i][:j]
        U[i][:j] = zeros[:j]

    return swaps

