
def smith_normal_decomp(m, domain=None):
    '''
    Return the Smith Normal Decomposition of a matrix `m` over the ring
    `domain`. This will only work if the ring is a principal ideal domain.

    Examples
    ========

    >>> from sympy import Matrix, ZZ
    >>> from sympy.matrices.normalforms import smith_normal_decomp
    >>> m = Matrix([[12, 6, 4], [3, 9, 6], [2, 16, 14]])
    >>> a, s, t = smith_normal_decomp(m, domain=ZZ)
    >>> assert a == s * m * t
    '''
    dM = _to_domain(m, domain)
    a, s, t = _snd(dM)
    return a.to_Matrix(), s.to_Matrix(), t.to_Matrix()


def smith_normal_decomp(m):
    '''
    Return the Smith-Normal form decomposition of matrix `m`.

    Examples
    ========

    >>> from sympy import ZZ
    >>> from sympy.polys.matrices import DomainMatrix
    >>> from sympy.polys.matrices.normalforms import smith_normal_decomp
    >>> m = DomainMatrix([[ZZ(12), ZZ(6), ZZ(4)],
    ...                   [ZZ(3), ZZ(9), ZZ(6)],
    ...                   [ZZ(2), ZZ(16), ZZ(14)]], (3, 3), ZZ)
    >>> a, s, t = smith_normal_decomp(m)
    >>> assert a == s * m * t
    '''
    domain = m.domain
    rows, cols = shape = m.shape
    m = m.to_list()

    invs, s, t = _smith_normal_decomp(m, domain, shape=shape, full=True)
    smf = DomainMatrix.diag(invs, domain, shape).to_dense()

    s = DomainMatrix(s, domain=domain, shape=(rows, rows))
    t = DomainMatrix(t, domain=domain, shape=(cols, cols))
    return smf, s, t

