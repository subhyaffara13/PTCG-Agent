
def _validate_array_cls(cls: type, sparse_ok=False) -> _ArrayClsInfo:
    if issubclass(cls, list | tuple):
        return _ArrayClsInfo.array_like

    # this comes from `_util._asarray_validated`
    if issubclass(cls, SparseABC):
        if not sparse_ok:
            msg = ('Sparse arrays/matrices are not supported by this function. '
                    'Perhaps one of the `scipy.sparse.linalg` functions '
                    'would work instead.')
            raise ValueError(msg)
        # `scipy.sparse` arrays are treated as compatible with NumPy
        # and assumed incompatible with other namespaces
        return _ArrayClsInfo.numpy

    if issubclass(cls, np.ma.MaskedArray):
        raise TypeError("Inputs of type `numpy.ma.MaskedArray` are not supported.")

    if issubclass(cls, np.matrix):
        raise TypeError("Inputs of type `numpy.matrix` are not supported.")

    if issubclass(cls, np.ndarray | np.generic):
        return _ArrayClsInfo.numpy

    # Note: this must happen after the test for np.generic, because
    # np.float64 and np.complex128 are subclasses of float and complex respectively.
    # This matches the behavior of array_api_compat.
    if issubclass(cls, int | float | complex | bool | type(None)):
        return _ArrayClsInfo.skip

    return _ArrayClsInfo.unknown

