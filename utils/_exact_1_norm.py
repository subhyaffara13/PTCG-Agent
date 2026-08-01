
def _exact_1_norm(A):
    # A compatibility function which should eventually disappear.
    if scipy.sparse.issparse(A):
        return max(abs(A).sum(axis=0).flat)
    elif is_pydata_spmatrix(A):
        return max(abs(A).sum(axis=0))
    else:
        return np.linalg.norm(A, 1)

