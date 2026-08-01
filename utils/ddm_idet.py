
def ddm_idet(a, K):
    """a  <--  echelon(a); return det

    Explanation
    ===========

    Compute the determinant of $a$ using the Bareiss fraction-free algorithm.
    The matrix $a$ is modified in place. Its diagonal elements are the
    determinants of the leading principal minors. The determinant of $a$ is
    returned.

    The domain $K$ must support exact division (``K.exquo``). This method is
    suitable for most exact rings and fields like :ref:`ZZ`, :ref:`QQ` and
    :ref:`QQ(a)` but not for inexact domains like :ref:`RR` and :ref:`CC`.

    Examples
    ========

    >>> from sympy import ZZ
    >>> from sympy.polys.matrices.ddm import ddm_idet
    >>> a = [[ZZ(1), ZZ(2), ZZ(3)], [ZZ(4), ZZ(5), ZZ(6)], [ZZ(7), ZZ(8), ZZ(9)]]
    >>> a
    [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    >>> ddm_idet(a, ZZ)
    0
    >>> a
    [[1, 2, 3], [4, -3, -6], [7, -6, 0]]
    >>> [a[i][i] for i in range(len(a))]
    [1, -3, 0]

    See Also
    ========

    sympy.polys.matrices.domainmatrix.DomainMatrix.det

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Bareiss_algorithm
    .. [2] https://www.math.usm.edu/perry/Research/Thesis_DRL.pdf
    """
    # Bareiss algorithm
    # https://www.math.usm.edu/perry/Research/Thesis_DRL.pdf

    # a is (m x n)
    m = len(a)
    if not m:
        return K.one
    n = len(a[0])

    exquo = K.exquo
    # uf keeps track of the sign change from row swaps
    uf = K.one

    for k in range(n-1):
        if not a[k][k]:
            for i in range(k+1, n):
                if a[i][k]:
                    a[k], a[i] = a[i], a[k]
                    uf = -uf
                    break
            else:
                return K.zero

        akkm1 = a[k-1][k-1] if k else K.one

        for i in range(k+1, n):
            for j in range(k+1, n):
                a[i][j] = exquo(a[i][j]*a[k][k] - a[i][k]*a[k][j], akkm1)

    return uf * a[-1][-1]

