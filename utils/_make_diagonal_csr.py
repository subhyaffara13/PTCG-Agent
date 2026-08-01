
def _make_diagonal_csr(data, is_array=False):
    """build diagonal csc_array/csr_array => self._csr_container

    Parameter `data` should be a raveled numpy array holding the
    values on the diagonal of the resulting sparse matrix.
    """
    from ._csr import csr_array, csr_matrix
    csr_array = csr_array if is_array else csr_matrix

    N = len(data)
    idx_dtype = get_index_dtype(maxval=N)
    indptr = np.arange(N + 1, dtype=idx_dtype)
    indices = indptr[:-1]

    return csr_array((data, indices, indptr), shape=(N, N))

