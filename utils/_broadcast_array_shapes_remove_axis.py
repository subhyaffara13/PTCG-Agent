
def _broadcast_array_shapes_remove_axis(arrays, axis=None):
    """
    Broadcast shapes of arrays, dropping specified axes

    Given a sequence of arrays `arrays` and an integer or tuple `axis`, find
    the shape of the broadcast result after consuming/dropping `axis`.
    In other words, return output shape of a typical hypothesis test on
    `arrays` vectorized along `axis`.

    Examples
    --------
    >>> import numpy as np
    >>> from scipy.stats._axis_nan_policy import _broadcast_array_shapes_remove_axis
    >>> a = np.zeros((5, 2, 1))
    >>> b = np.zeros((9, 3))
    >>> _broadcast_array_shapes_remove_axis((a, b), 1)
    (5, 3)
    """
    # Note that here, `axis=None` means do not consume/drop any axes - _not_
    # ravel arrays before broadcasting.
    shapes = [arr.shape for arr in arrays]
    return _broadcast_shapes_remove_axis(shapes, axis)

