
def _LDLdecomposition_sparse(M, hermitian=True):
    """
    Returns the LDL Decomposition (matrices ``L`` and ``D``) of matrix
    ``A``, such that ``L * D * L.T == A``. ``A`` must be a square,
    symmetric, positive-definite and non-singular.

    This method eliminates the use of square root and ensures that all
    the diagonal entries of L are 1.

    Examples
    ========

    >>> from sympy import SparseMatrix
    >>> A = SparseMatrix(((25, 15, -5), (15, 18, 0), (-5, 0, 11)))
    >>> L, D = A.LDLdecomposition()
    >>> L
    Matrix([
    [   1,   0, 0],
    [ 3/5,   1, 0],
    [-1/5, 1/3, 1]])
    >>> D
    Matrix([
    [25, 0, 0],
    [ 0, 9, 0],
    [ 0, 0, 9]])
    >>> L * D * L.T == A
    True

    """

    from .dense import MutableDenseMatrix

    if not M.is_square:
        raise NonSquareMatrixError("Matrix must be square.")
    if hermitian and not M.is_hermitian:
        raise ValueError("Matrix must be Hermitian.")
    if not hermitian and not M.is_symmetric():
        raise ValueError("Matrix must be symmetric.")

    dps       = _get_intermediate_simp(expand_mul, expand_mul)
    Lrowstruc = M.row_structure_symbolic_cholesky()
    L         = MutableDenseMatrix.eye(M.rows)
    D         = MutableDenseMatrix.zeros(M.rows, M.cols)

    for i in range(len(Lrowstruc)):
        for j in Lrowstruc[i]:
            if i != j:
                L[i, j] = M[i, j]
                summ    = 0

                for p1 in Lrowstruc[i]:
                    if p1 < j:
                        for p2 in Lrowstruc[j]:
                            if p2 < j:
                                if p1 == p2:
                                    if hermitian:
                                        summ += L[i, p1]*L[j, p1].conjugate()*D[p1, p1]
                                    else:
                                        summ += L[i, p1]*L[j, p1]*D[p1, p1]
                            else:
                                break
                    else:
                        break

                L[i, j] = dps((L[i, j] - summ) / D[j, j])

            else: # i == j
                D[i, i] = M[i, i]
                summ    = 0

                for k in Lrowstruc[i]:
                    if k < i:
                        if hermitian:
                            summ += L[i, k]*L[i, k].conjugate()*D[k, k]
                        else:
                            summ += L[i, k]**2*D[k, k]
                    else:
                        break

                D[i, i] = dps(D[i, i] - summ)

                if hermitian and D[i, i].is_positive is False:
                    raise NonPositiveDefiniteMatrixError(
                        "Matrix must be positive-definite")

    return M._new(L), M._new(D)

