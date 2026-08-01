
def _todata(s) -> np.ndarray:
    """Access nonzero values, possibly after summing duplicates.

    Parameters
    ----------
    s : sparse array
        Input sparse array.

    Returns
    -------
    data: ndarray
      Nonzero values of the array, with shape (s.nnz,)

    """
    if isinstance(s, sp._data._data_matrix):
        return s._deduped_data()

    if isinstance(s, sp.dok_array):
        return np.fromiter(s.values(), dtype=s.dtype, count=s.nnz)

    if isinstance(s, sp.lil_array):
        data = np.empty(s.nnz, dtype=s.dtype)
        sp._csparsetools.lil_flatten_to_array(s.data, data)
        return data

    return s.tocoo()._deduped_data()

