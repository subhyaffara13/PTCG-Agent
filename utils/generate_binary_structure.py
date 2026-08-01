
def generate_binary_structure(rank, connectivity):
    """
    Generate a binary structure for binary morphological operations.

    Parameters
    ----------
    rank : int
         Number of dimensions of the array to which the structuring element
         will be applied, as returned by `np.ndim`.
    connectivity : int
         `connectivity` determines which elements of the output array belong
         to the structure, i.e., are considered as neighbors of the central
         element. Elements up to a squared distance of `connectivity` from
         the center are considered neighbors. `connectivity` may range from 1
         (no diagonal elements are neighbors) to `rank` (all elements are
         neighbors).

    Returns
    -------
    output : ndarray of bools
         Structuring element which may be used for binary morphological
         operations, with `rank` dimensions and all dimensions equal to 3.

    See Also
    --------
    iterate_structure, binary_dilation, binary_erosion

    Notes
    -----
    `generate_binary_structure` can only create structuring elements with
    dimensions equal to 3, i.e., minimal dimensions. For larger structuring
    elements, that are useful e.g., for eroding large objects, one may either
    use `iterate_structure`, or create directly custom arrays with
    numpy functions such as `numpy.ones`.

    Examples
    --------
    >>> from scipy import ndimage
    >>> import numpy as np
    >>> struct = ndimage.generate_binary_structure(2, 1)
    >>> struct
    array([[False,  True, False],
           [ True,  True,  True],
           [False,  True, False]], dtype=bool)
    >>> a = np.zeros((5,5))
    >>> a[2, 2] = 1
    >>> a
    array([[ 0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  1.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  0.]])
    >>> b = ndimage.binary_dilation(a, structure=struct).astype(a.dtype)
    >>> b
    array([[ 0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  1.,  0.,  0.],
           [ 0.,  1.,  1.,  1.,  0.],
           [ 0.,  0.,  1.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  0.]])
    >>> ndimage.binary_dilation(b, structure=struct).astype(a.dtype)
    array([[ 0.,  0.,  1.,  0.,  0.],
           [ 0.,  1.,  1.,  1.,  0.],
           [ 1.,  1.,  1.,  1.,  1.],
           [ 0.,  1.,  1.,  1.,  0.],
           [ 0.,  0.,  1.,  0.,  0.]])
    >>> struct = ndimage.generate_binary_structure(2, 2)
    >>> struct
    array([[ True,  True,  True],
           [ True,  True,  True],
           [ True,  True,  True]], dtype=bool)
    >>> struct = ndimage.generate_binary_structure(3, 1)
    >>> struct # no diagonal elements
    array([[[False, False, False],
            [False,  True, False],
            [False, False, False]],
           [[False,  True, False],
            [ True,  True,  True],
            [False,  True, False]],
           [[False, False, False],
            [False,  True, False],
            [False, False, False]]], dtype=bool)

    """
    if connectivity < 1:
        connectivity = 1
    if rank < 1:
        return np.array(True, dtype=bool)
    output = np.fabs(np.indices([3] * rank) - 1)
    output = np.add.reduce(output, 0)
    return output <= connectivity

