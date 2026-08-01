
def _is_positive_semidefinite_cholesky(M):
    """Uses Cholesky factorization with complete pivoting

    References
    ==========

    .. [1] http://eprints.ma.man.ac.uk/1199/1/covered/MIMS_ep2008_116.pdf

    .. [2] https://www.value-at-risk.net/cholesky-factorization/
    """
    M = M.as_mutable()
    for k in range(M.rows):
        diags = [M[i, i] for i in range(k, M.rows)]
        pivot, pivot_val, nonzero, _ = _find_reasonable_pivot(diags)

        if nonzero:
            return None

        if pivot is None:
            for i in range(k+1, M.rows):
                for j in range(k, M.cols):
                    iszero = M[i, j].is_zero
                    if iszero is None:
                        return None
                    elif iszero is False:
                        return False
            return True

        if M[k, k].is_negative or pivot_val.is_negative:
            return False
        elif not (M[k, k].is_nonnegative and pivot_val.is_nonnegative):
            return None

        if pivot > 0:
            M.col_swap(k, k+pivot)
            M.row_swap(k, k+pivot)

        M[k, k] = sqrt(M[k, k])
        M[k, k+1:] /= M[k, k]
        M[k+1:, k+1:] -= M[k, k+1:].H * M[k, k+1:]

    return M[-1, -1].is_nonnegative

