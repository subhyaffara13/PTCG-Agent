
def transpose_homogeneous_pyarrow(
    arrays: Sequence[ArrowExtensionArray],
) -> list[ArrowExtensionArray]:
    """Transpose arrow extension arrays in a list, but faster.

    Input should be a list of arrays of equal length and all have the same
    dtype. The caller is responsible for ensuring validity of input data.
    """
    arrays = list(arrays)
    nrows, ncols = len(arrays[0]), len(arrays)
    indices = np.arange(nrows * ncols).reshape(ncols, nrows).T.reshape(-1)
    arr = pa.chunked_array([chunk for arr in arrays for chunk in arr._pa_array.chunks])
    arr = arr.take(indices)
    return [ArrowExtensionArray(arr.slice(i * ncols, ncols)) for i in range(nrows)]

