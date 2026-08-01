
def _is_upper_triangular(A):
    # This function could possibly be of wider interest.
    if issparse(A):
        lower_part = scipy.sparse.tril(A, -1)
        # Check structural upper triangularity,
        # then coincidental upper triangularity if needed.
        return lower_part.nnz == 0 or lower_part.count_nonzero() == 0
    elif is_pydata_spmatrix(A):
        import sparse
        lower_part = sparse.tril(A, -1)
        return lower_part.nnz == 0
    else:
        return not np.tril(A, -1).any()

