
def _row_structure_symbolic_cholesky(M):
    """Symbolic cholesky factorization, for pre-determination of the
    non-zero structure of the Cholesky factororization.

    Examples
    ========

    >>> from sympy import SparseMatrix
    >>> S = SparseMatrix([
    ... [1, 0, 3, 2],
    ... [0, 0, 1, 0],
    ... [4, 0, 0, 5],
    ... [0, 6, 7, 0]])
    >>> S.row_structure_symbolic_cholesky()
    [[0], [], [0], [1, 2]]

    References
    ==========

    .. [1] Symbolic Sparse Cholesky Factorization using Elimination Trees,
           Jeroen Van Grondelle (1999)
           https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.39.7582
    """

    R, parent = M.liupc()
    inf       = len(R)  # this acts as infinity
    Lrow      = copy.deepcopy(R)

    for k in range(M.rows):
        for j in R[k]:
            while j != inf and j != k:
                Lrow[k].append(j)
                j = parent[j]

        Lrow[k] = sorted(set(Lrow[k]))

    return Lrow

