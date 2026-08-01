
def _block_concatenate(arrays, list_ndim, result_ndim):
    result = _block(arrays, list_ndim, result_ndim)
    if list_ndim == 0:
        # Catch an edge case where _block returns a view because
        # `arrays` is a single numpy array and not a list of numpy arrays.
        # This might copy scalars or lists twice, but this isn't a likely
        # usecase for those interested in performance
        result = result.copy()
    return result

