
def _fast_spmatrix_to_csc(A, hermitian=False):
    """Convert sparse matrix to CSC (by transposing, if possible)"""
    if (A.format == "csr" and hermitian
            and not np.issubdtype(A.dtype, np.complexfloating)):
        return A.T
    elif is_pydata_spmatrix(A):
        # No need to convert
        return A
    else:
        return A.tocsc()

