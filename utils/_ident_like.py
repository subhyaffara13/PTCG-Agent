
def _ident_like(A):
    # A compatibility function which should eventually disappear.
    if scipy.sparse.issparse(A):
        # Creates a sparse matrix in dia format
        out = scipy.sparse.eye(A.shape[0], A.shape[1], dtype=A.dtype)
        if scipy.sparse.issparse(A):
            return out.asformat(A.format)
        return scipy.sparse.dia_array(out).asformat(A.format)
    elif is_pydata_spmatrix(A):
        import sparse
        return sparse.eye(A.shape[0], A.shape[1], dtype=A.dtype)
    elif isinstance(A, scipy.sparse.linalg.LinearOperator):
        return IdentityOperator(A.shape, dtype=A.dtype)
    else:
        return np.eye(A.shape[0], A.shape[1], dtype=A.dtype)

