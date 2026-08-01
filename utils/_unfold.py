
def _unfold(arr, axis, size, step):
    """
    Append an extra dimension containing sliding windows along *axis*.

    All windows are of size *size* and begin with every *step* elements.

    Parameters
    ----------
    arr : ndarray, shape (N_1, ..., N_k)
        The input array
    axis : int
        Axis along which the windows are extracted
    size : int
        Size of the windows
    step : int
        Stride between first elements of subsequent windows.

    Returns
    -------
    ndarray, shape (N_1, ..., 1 + (N_axis-size)/step, ..., N_k, size)

    Examples
    --------
    >>> i, j = np.ogrid[:3, :7]
    >>> a = i*10 + j
    >>> a
    array([[ 0,  1,  2,  3,  4,  5,  6],
           [10, 11, 12, 13, 14, 15, 16],
           [20, 21, 22, 23, 24, 25, 26]])
    >>> _unfold(a, axis=1, size=3, step=2)
    array([[[ 0,  1,  2],
            [ 2,  3,  4],
            [ 4,  5,  6]],
           [[10, 11, 12],
            [12, 13, 14],
            [14, 15, 16]],
           [[20, 21, 22],
            [22, 23, 24],
            [24, 25, 26]]])
    """
    new_shape = [*arr.shape, size]
    new_strides = [*arr.strides, arr.strides[axis]]
    new_shape[axis] = (new_shape[axis] - size) // step + 1
    new_strides[axis] = new_strides[axis] * step
    return np.lib.stride_tricks.as_strided(arr,
                                           shape=new_shape,
                                           strides=new_strides,
                                           writeable=False)


def _unfold(array: np.ndarray, dimension: int, size: int, step: int) -> np.ndarray:
    """A basic NumPy equivalent of PyTorch's unfold for 2D arrays along the last dim."""
    if array.ndim != 2:
        raise ValueError("This unfold implementation currently supports 2D arrays (batch, time).")
    if dimension != -1 and dimension != array.ndim - 1:
        raise ValueError("This unfold implementation only supports unfolding the last dimension.")

    batch_size, original_length = array.shape
    num_frames = (original_length - size) // step + 1

    if num_frames <= 0:
        return np.zeros((batch_size, 0, size), dtype=array.dtype)

    output_shape = (batch_size, num_frames, size)
    output_strides = (array.strides[0], array.strides[1] * step, array.strides[1])

    return np.lib.stride_tricks.as_strided(array, shape=output_shape, strides=output_strides)


def _unfold(array: np.ndarray, dimension: int, size: int, step: int) -> np.ndarray:
    """A basic NumPy equivalent of PyTorch's unfold for 2D arrays along the last dim."""
    if array.ndim != 2:
        raise ValueError("This unfold implementation currently supports 2D arrays (batch, time).")
    if dimension != -1 and dimension != array.ndim - 1:
        raise ValueError("This unfold implementation only supports unfolding the last dimension.")

    batch_size, original_length = array.shape
    num_frames = (original_length - size) // step + 1

    if num_frames <= 0:
        return np.zeros((batch_size, 0, size), dtype=array.dtype)

    output_shape = (batch_size, num_frames, size)
    output_strides = (array.strides[0], array.strides[1] * step, array.strides[1])

    return np.lib.stride_tricks.as_strided(array, shape=output_shape, strides=output_strides)

