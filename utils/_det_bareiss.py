
def _det_bareiss(M, iszerofunc=_is_zero_after_expand_mul):
    """Compute matrix determinant using Bareiss' fraction-free
    algorithm which is an extension of the well known Gaussian
    elimination method. This approach is best suited for dense
    symbolic matrices and will result in a determinant with
    minimal number of fractions. It means that less term
    rewriting is needed on resulting formulae.

    Parameters
    ==========

    iszerofunc : function, optional
        The function to use to determine zeros when doing an LU decomposition.
        Defaults to ``lambda x: x.is_zero``.

    TODO: Implement algorithm for sparse matrices (SFF),
    http://www.eecis.udel.edu/~saunders/papers/sffge/it5.ps.
    """

    # Recursively implemented Bareiss' algorithm as per Deanna Richelle Leggett's
    # thesis http://www.math.usm.edu/perry/Research/Thesis_DRL.pdf
    def bareiss(mat, cumm=1):
        if mat.rows == 0:
            return mat.one
        elif mat.rows == 1:
            return mat[0, 0]

        # find a pivot and extract the remaining matrix
        # With the default iszerofunc, _find_reasonable_pivot slows down
        # the computation by the factor of 2.5 in one test.
        # Relevant issues: #10279 and #13877.
        pivot_pos, pivot_val, _, _ = _find_reasonable_pivot(mat[:, 0], iszerofunc=iszerofunc)
        if pivot_pos is None:
            return mat.zero

        # if we have a valid pivot, we'll do a "row swap", so keep the
        # sign of the det
        sign = (-1) ** (pivot_pos % 2)

        # we want every row but the pivot row and every column
        rows = [i for i in range(mat.rows) if i != pivot_pos]
        cols = list(range(mat.cols))
        tmp_mat = mat.extract(rows, cols)

        def entry(i, j):
            ret = (pivot_val*tmp_mat[i, j + 1] - mat[pivot_pos, j + 1]*tmp_mat[i, 0]) / cumm
            if _get_intermediate_simp_bool(True):
                return _dotprodsimp(ret)
            elif not ret.is_Atom:
                return cancel(ret)
            return ret

        return sign*bareiss(M._new(mat.rows - 1, mat.cols - 1, entry), pivot_val)

    if not M.is_square:
        raise NonSquareMatrixError()

    if M.rows == 0:
        return M.one
        # sympy/matrices/tests/test_matrices.py contains a test that
        # suggests that the determinant of a 0 x 0 matrix is one, by
        # convention.

    return bareiss(M)

