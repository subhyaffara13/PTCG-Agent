
def _liupc(M):
    """Liu's algorithm, for pre-determination of the Elimination Tree of
    the given matrix, used in row-based symbolic Cholesky factorization.

    Examples
    ========

    >>> from sympy import SparseMatrix
    >>> S = SparseMatrix([
    ... [1, 0, 3, 2],
    ... [0, 0, 1, 0],
    ... [4, 0, 0, 5],
    ... [0, 6, 7, 0]])
    >>> S.liupc()
    ([[0], [], [0], [1, 2]], [4, 3, 4, 4])

    References
    ==========

    .. [1] Symbolic Sparse Cholesky Factorization using Elimination Trees,
           Jeroen Van Grondelle (1999)
           https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.39.7582
    """
    # Algorithm 2.4, p 17 of reference

    # get the indices of the elements that are non-zero on or below diag
    R = [[] for r in range(M.rows)]

    for r, c, _ in M.row_list():
        if c <= r:
            R[r].append(c)

    inf     = len(R)  # nothing will be this large
    parent  = [inf]*M.rows
    virtual = [inf]*M.rows

    for r in range(M.rows):
        for c in R[r][:-1]:
            while virtual[c] < r:
                t          = virtual[c]
                virtual[c] = r
                c          = t

            if virtual[c] == inf:
                parent[c] = virtual[c] = r

    return R, parent

