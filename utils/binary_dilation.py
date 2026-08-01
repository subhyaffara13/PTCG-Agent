
def binary_dilation(input, structure=None, iterations=1, mask=None,
                    output=None, border_value=0, origin=0,
                    brute_force=False, *, axes=None):
    """
    Multidimensional binary dilation with the given structuring element.

    Parameters
    ----------
    input : array_like
        Binary array_like to be dilated. Non-zero (True) elements form
        the subset to be dilated.
    structure : array_like, optional
        Structuring element used for the dilation. Non-zero elements are
        considered True. If no structuring element is provided an element
        is generated with a square connectivity equal to one.
    iterations : int, optional
        The dilation is repeated `iterations` times (one, by default).
        If iterations is less than 1, the dilation is repeated until the
        result does not change anymore. Only an integer of iterations is
        accepted.
    mask : array_like, optional
        If a mask is given, only those elements with a True value at
        the corresponding mask element are modified at each iteration.
    output : ndarray, optional
        Array of the same shape as input, into which the output is placed.
        By default, a new array is created.
    border_value : int (cast to 0 or 1), optional
        Value at the border in the output array.
    origin : int or tuple of ints, optional
        Placement of the filter, by default 0.
    brute_force : bool, optional
        Memory condition: if False, only the pixels whose value was changed in
        the last iteration are tracked as candidates to be updated (dilated)
        in the current iteration; if True all pixels are considered as
        candidates for dilation, regardless of what happened in the previous
        iteration. False by default.
    axes : tuple of int or None
        The axes over which to apply the filter. If None, `input` is filtered
        along all axes. If an `origin` tuple is provided, its length must match
        the number of axes.

    Returns
    -------
    binary_dilation : ndarray of bools
        Dilation of the input by the structuring element.

    See Also
    --------
    grey_dilation, binary_erosion, binary_closing, binary_opening,
    generate_binary_structure

    Notes
    -----
    Dilation [1]_ is a mathematical morphology operation [2]_ that uses a
    structuring element for expanding the shapes in an image. The binary
    dilation of an image by a structuring element is the locus of the points
    covered by the structuring element, when its center lies within the
    non-zero points of the image.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Dilation_%28morphology%29
    .. [2] https://en.wikipedia.org/wiki/Mathematical_morphology

    Examples
    --------
    >>> from scipy import ndimage
    >>> import numpy as np
    >>> a = np.zeros((5, 5))
    >>> a[2, 2] = 1
    >>> a
    array([[ 0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  1.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  0.]])
    >>> ndimage.binary_dilation(a)
    array([[False, False, False, False, False],
           [False, False,  True, False, False],
           [False,  True,  True,  True, False],
           [False, False,  True, False, False],
           [False, False, False, False, False]], dtype=bool)
    >>> ndimage.binary_dilation(a).astype(a.dtype)
    array([[ 0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  1.,  0.,  0.],
           [ 0.,  1.,  1.,  1.,  0.],
           [ 0.,  0.,  1.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  0.]])
    >>> # 3x3 structuring element with connectivity 1, used by default
    >>> struct1 = ndimage.generate_binary_structure(2, 1)
    >>> struct1
    array([[False,  True, False],
           [ True,  True,  True],
           [False,  True, False]], dtype=bool)
    >>> # 3x3 structuring element with connectivity 2
    >>> struct2 = ndimage.generate_binary_structure(2, 2)
    >>> struct2
    array([[ True,  True,  True],
           [ True,  True,  True],
           [ True,  True,  True]], dtype=bool)
    >>> ndimage.binary_dilation(a, structure=struct1).astype(a.dtype)
    array([[ 0.,  0.,  0.,  0.,  0.],
           [ 0.,  0.,  1.,  0.,  0.],
           [ 0.,  1.,  1.,  1.,  0.],
           [ 0.,  0.,  1.,  0.,  0.],
           [ 0.,  0.,  0.,  0.,  0.]])
    >>> ndimage.binary_dilation(a, structure=struct2).astype(a.dtype)
    array([[ 0.,  0.,  0.,  0.,  0.],
           [ 0.,  1.,  1.,  1.,  0.],
           [ 0.,  1.,  1.,  1.,  0.],
           [ 0.,  1.,  1.,  1.,  0.],
           [ 0.,  0.,  0.,  0.,  0.]])
    >>> ndimage.binary_dilation(a, structure=struct1,\\
    ... iterations=2).astype(a.dtype)
    array([[ 0.,  0.,  1.,  0.,  0.],
           [ 0.,  1.,  1.,  1.,  0.],
           [ 1.,  1.,  1.,  1.,  1.],
           [ 0.,  1.,  1.,  1.,  0.],
           [ 0.,  0.,  1.,  0.,  0.]])

    """
    input = np.asarray(input)
    axes = _ni_support._check_axes(axes, input.ndim)
    num_axes = len(axes)
    if structure is None:
        structure = generate_binary_structure(num_axes, 1)
    origin = _ni_support._normalize_sequence(origin, num_axes)
    structure = np.asarray(structure)
    structure = structure[tuple([slice(None, None, -1)] *
                                structure.ndim)]
    for ii in range(len(origin)):
        origin[ii] = -origin[ii]
        if not structure.shape[ii] & 1:
            origin[ii] -= 1

    return _binary_erosion(input, structure, iterations, mask,
                           output, border_value, origin, 1, brute_force, axes)

