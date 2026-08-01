
def _det_LU(M, iszerofunc=_iszero, simpfunc=None):
    """ Computes the determinant of a matrix from its LU decomposition.
    This function uses the LU decomposition computed by
    LUDecomposition_Simple().

    The keyword arguments iszerofunc and simpfunc are passed to
    LUDecomposition_Simple().
    iszerofunc is a callable that returns a boolean indicating if its
    input is zero, or None if it cannot make the determination.
    simpfunc is a callable that simplifies its input.
    The default is simpfunc=None, which indicate that the pivot search
    algorithm should not attempt to simplify any candidate pivots.
    If simpfunc fails to simplify its input, then it must return its input
    instead of a copy.

    Parameters
    ==========

    iszerofunc : function, optional
        The function to use to determine zeros when doing an LU decomposition.
        Defaults to ``lambda x: x.is_zero``.

    simpfunc : function, optional
        The simplification function to use when looking for zeros for pivots.
    """

    if not M.is_square:
        raise NonSquareMatrixError()

    if M.rows == 0:
        return M.one
        # sympy/matrices/tests/test_matrices.py contains a test that
        # suggests that the determinant of a 0 x 0 matrix is one, by
        # convention.

    lu, row_swaps = M.LUdecomposition_Simple(iszerofunc=iszerofunc,
            simpfunc=simpfunc)
    # P*A = L*U => det(A) = det(L)*det(U)/det(P) = det(P)*det(U).
    # Lower triangular factor L encoded in lu has unit diagonal => det(L) = 1.
    # P is a permutation matrix => det(P) in {-1, 1} => 1/det(P) = det(P).
    # LUdecomposition_Simple() returns a list of row exchange index pairs, rather
    # than a permutation matrix, but det(P) = (-1)**len(row_swaps).

    # Avoid forming the potentially time consuming  product of U's diagonal entries
    # if the product is zero.
    # Bottom right entry of U is 0 => det(A) = 0.
    # It may be impossible to determine if this entry of U is zero when it is symbolic.
    if iszerofunc(lu[lu.rows-1, lu.rows-1]):
        return M.zero

    # Compute det(P)
    det = -M.one if len(row_swaps)%2 else M.one

    # Compute det(U) by calculating the product of U's diagonal entries.
    # The upper triangular portion of lu is the upper triangular portion of the
    # U factor in the LU decomposition.
    for k in range(lu.rows):
        det *= lu[k, k]

    # return det(P)*det(U)
    return det

