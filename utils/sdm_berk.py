
def sdm_berk(M, n, K):
    """
    Berkowitz algorithm for computing the characteristic polynomial.

    Explanation
    ===========

    The Berkowitz algorithm is a division-free algorithm for computing the
    characteristic polynomial of a matrix over any commutative ring using only
    arithmetic in the coefficient ring. This implementation is for sparse
    matrices represented in a dict-of-dicts format (like :class:`SDM`).

    Examples
    ========

    >>> from sympy import Matrix
    >>> from sympy.polys.matrices.sdm import sdm_berk
    >>> from sympy.polys.domains import ZZ
    >>> M = {0: {0: ZZ(1), 1:ZZ(2)}, 1: {0:ZZ(3), 1:ZZ(4)}}
    >>> sdm_berk(M, 2, ZZ)
    {0: 1, 1: -5, 2: -2}
    >>> Matrix([[1, 2], [3, 4]]).charpoly()
    PurePoly(lambda**2 - 5*lambda - 2, lambda, domain='ZZ')

    See Also
    ========

    sympy.polys.matrices.domainmatrix.DomainMatrix.charpoly
        The high-level interface to this function.
    sympy.polys.matrices.dense.ddm_berk
        The dense version of this function.

    References
    ==========

    .. [1] https://en.wikipedia.org/wiki/Samuelson%E2%80%93Berkowitz_algorithm
    """
    zero = K.zero
    one = K.one

    if n == 0:
        return {0: one}
    elif n == 1:
        pdict = {0: one}
        if M00 := M.get(0, {}).get(0, zero):
            pdict[1] = -M00

    # M = [[a, R],
    #      [C, A]]
    a, R, C, A = K.zero, {}, {}, defaultdict(dict)
    for i, Mi in M.items():
        for j, Mij in Mi.items():
            if i and j:
                A[i-1][j-1] = Mij
            elif i:
                C[i-1] = Mij
            elif j:
                R[j-1] = Mij
            else:
                a = Mij

    # T = [       1,      0,    0,  0, 0, ... ]
    #     [      -a,      1,    0,  0, 0, ... ]
    #     [    -R*C,     -a,    1,  0, 0, ... ]
    #     [  -R*A*C,   -R*C,   -a,  1, 0, ... ]
    #     [-R*A^2*C, -R*A*C, -R*C, -a, 1, ... ]
    #     [ ...                               ]
    # T is (n+1) x n
    #
    # In the sparse case we might have A^m*C = 0 for some m making T banded
    # rather than triangular so we just compute the nonzero entries of the
    # first column rather than constructing the matrix explicitly.

    AnC = C
    RC = sdm_dotvec(R, C, K)

    Tvals = [one, -a, -RC]
    for i in range(3, n+1):
        AnC = sdm_matvecmul(A, AnC, K)
        if not AnC:
            break
        RAnC = sdm_dotvec(R, AnC, K)
        Tvals.append(-RAnC)

    # Strip trailing zeros
    while Tvals and not Tvals[-1]:
        Tvals.pop()

    q = sdm_berk(A, n-1, K)

    # This would be the explicit multiplication T*q but we can do better:
    #
    #  T = {}
    #  for i in range(n+1):
    #      Ti = {}
    #      for j in range(max(0, i-len(Tvals)+1), min(i+1, n)):
    #          Ti[j] = Tvals[i-j]
    #      T[i] = Ti
    #  Tq = sdm_matvecmul(T, q, K)
    #
    # In the sparse case q might be mostly zero. We know that T[i,j] is nonzero
    # for i <= j < i + len(Tvals) so if q does not have a nonzero entry in that
    # range then Tq[j] must be zero. We exploit this potential banded
    # structure and the potential sparsity of q to compute Tq more efficiently.

    Tvals = Tvals[::-1]

    Tq = {}

    for i in range(min(q), min(max(q)+len(Tvals), n+1)):
        Ti = dict(enumerate(Tvals, i-len(Tvals)+1))
        if Tqi := sdm_dotvec(Ti, q, K):
            Tq[i] = Tqi

    return Tq

