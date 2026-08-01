
def ddm_iinv(ainv, a, K):
    """ainv  <--  inv(a)

    Compute the inverse of a matrix $a$ over a field $K$ using Gauss-Jordan
    elimination. The result is stored in $ainv$.

    Uses division in the ground domain which should be an exact field.

    Examples
    ========

    >>> from sympy.polys.matrices.ddm import ddm_iinv, ddm_imatmul
    >>> from sympy import QQ
    >>> a = [[QQ(1), QQ(2)], [QQ(3), QQ(4)]]
    >>> ainv = [[None, None], [None, None]]
    >>> ddm_iinv(ainv, a, QQ)
    >>> ainv
    [[-2, 1], [3/2, -1/2]]
    >>> result = [[QQ(0), QQ(0)], [QQ(0), QQ(0)]]
    >>> ddm_imatmul(result, a, ainv)
    >>> result
    [[1, 0], [0, 1]]

    See Also
    ========

    ddm_irref: the underlying routine.
    """
    if not K.is_Field:
        raise DMDomainError('Not a field')

    # a is (m x n)
    m = len(a)
    if not m:
        return
    n = len(a[0])
    if m != n:
        raise DMNonSquareMatrixError

    eye = [[K.one if i==j else K.zero for j in range(n)] for i in range(n)]
    Aaug = [row + eyerow for row, eyerow in zip(a, eye)]
    pivots = ddm_irref(Aaug)
    if pivots != list(range(n)):
        raise DMNonInvertibleMatrixError('Matrix det == 0; not invertible.')
    ainv[:] = [row[n:] for row in Aaug]

