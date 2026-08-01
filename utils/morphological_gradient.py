
def morphological_gradient(input, size=None, footprint=None, structure=None,
                           output=None, mode="reflect", cval=0.0, origin=0, *,
                           axes=None):
    """
    Multidimensional morphological gradient.

    The morphological gradient is calculated as the difference between a
    dilation and an erosion of the input with a given structuring element.

    Parameters
    ----------
    input : array_like
        Array over which to compute the morphological gradient.
    size : tuple of ints
        Shape of a flat and full structuring element used for the mathematical
        morphology operations. Optional if `footprint` or `structure` is
        provided. A larger `size` yields a more blurred gradient.
    footprint : array of ints, optional
        Positions of non-infinite elements of a flat structuring element
        used for the morphology operations. Larger footprints
        give a more blurred morphological gradient.
    structure : array of ints, optional
        Structuring element used for the morphology operations. `structure` may
        be a non-flat structuring element. The `structure` array applies
        offsets to the pixels in a neighborhood (the offset is additive during
        dilation and subtractive during erosion)
    output : array, optional
        An array used for storing the output of the morphological gradient
        may be provided.
    mode : {'reflect', 'constant', 'nearest', 'mirror', 'wrap'}, optional
        The `mode` parameter determines how the array borders are
        handled, where `cval` is the value when mode is equal to
        'constant'. Default is 'reflect'
    cval : scalar, optional
        Value to fill past edges of input if `mode` is 'constant'. Default
        is 0.0.
    origin : scalar, optional
        The `origin` parameter controls the placement of the filter.
        Default 0
    axes : tuple of int or None
        The axes over which to apply the filter. If None, `input` is filtered
        along all axes. If an `origin` tuple is provided, its length must match
        the number of axes.

    Returns
    -------
    morphological_gradient : ndarray
        Morphological gradient of `input`.

    See Also
    --------
    grey_dilation, grey_erosion, gaussian_gradient_magnitude

    Notes
    -----
    For a flat structuring element, the morphological gradient
    computed at a given point corresponds to the maximal difference
    between elements of the input among the elements covered by the
    structuring element centered on the point.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Mathematical_morphology

    Examples
    --------
    >>> from scipy import ndimage
    >>> import numpy as np
    >>> a = np.zeros((7,7), dtype=int)
    >>> a[2:5, 2:5] = 1
    >>> ndimage.morphological_gradient(a, size=(3,3))
    array([[0, 0, 0, 0, 0, 0, 0],
           [0, 1, 1, 1, 1, 1, 0],
           [0, 1, 1, 1, 1, 1, 0],
           [0, 1, 1, 0, 1, 1, 0],
           [0, 1, 1, 1, 1, 1, 0],
           [0, 1, 1, 1, 1, 1, 0],
           [0, 0, 0, 0, 0, 0, 0]])
    >>> # The morphological gradient is computed as the difference
    >>> # between a dilation and an erosion
    >>> ndimage.grey_dilation(a, size=(3,3)) -\\
    ...  ndimage.grey_erosion(a, size=(3,3))
    array([[0, 0, 0, 0, 0, 0, 0],
           [0, 1, 1, 1, 1, 1, 0],
           [0, 1, 1, 1, 1, 1, 0],
           [0, 1, 1, 0, 1, 1, 0],
           [0, 1, 1, 1, 1, 1, 0],
           [0, 1, 1, 1, 1, 1, 0],
           [0, 0, 0, 0, 0, 0, 0]])
    >>> a = np.zeros((7,7), dtype=int)
    >>> a[2:5, 2:5] = 1
    >>> a[4,4] = 2; a[2,3] = 3
    >>> a
    array([[0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0],
           [0, 0, 1, 3, 1, 0, 0],
           [0, 0, 1, 1, 1, 0, 0],
           [0, 0, 1, 1, 2, 0, 0],
           [0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0]])
    >>> ndimage.morphological_gradient(a, size=(3,3))
    array([[0, 0, 0, 0, 0, 0, 0],
           [0, 1, 3, 3, 3, 1, 0],
           [0, 1, 3, 3, 3, 1, 0],
           [0, 1, 3, 2, 3, 2, 0],
           [0, 1, 1, 2, 2, 2, 0],
           [0, 1, 1, 2, 2, 2, 0],
           [0, 0, 0, 0, 0, 0, 0]])

    """
    tmp = grey_dilation(input, size, footprint, structure, None, mode,
                        cval, origin, axes=axes)
    if isinstance(output, np.ndarray):
        grey_erosion(input, size, footprint, structure, output, mode,
                     cval, origin, axes=axes)
        return np.subtract(tmp, output, output)
    else:
        return (tmp - grey_erosion(input, size, footprint, structure,
                                   None, mode, cval, origin, axes=axes))

