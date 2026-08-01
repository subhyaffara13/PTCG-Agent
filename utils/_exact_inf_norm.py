
def _exact_inf_norm(A):
    # A compatibility function which should eventually disappear.
    if scipy.sparse.issparse(A):
        return max(abs(A).sum(axis=1).flat)
    elif is_pydata_spmatrix(A):
        return max(abs(A).sum(axis=1))
    else:
        return np.linalg.norm(A, np.inf)

