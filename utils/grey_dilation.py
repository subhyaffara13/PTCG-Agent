
def grey_dilation(input, size=None, footprint=None, structure=None,
                  output=None, mode="reflect", cval=0.0, origin=0, *,
                  axes=None):
    """
    Calculate a greyscale dilation, using either a structuring element,
    or a footprint corresponding to a flat structuring element.

    Grayscale dilation is a mathematical morphology operation. For the
    simple case of a full and flat structuring element, it can be viewed
    as a maximum filter over a sliding window.

    Parameters
    ----------
    input : array_like
        Array over which the grayscale dilation is to be computed.
    size : tuple of ints
        Shape of a flat and full structuring element used for the grayscale
        dilation. Optional if `footprint` or `structure` is provided.
    footprint : array of ints, optional
        Positions of non-infinite elements of a flat structuring element
        used for the grayscale dilation. Non-zero values give the set of
        neighbors of the center over which the maximum is chosen.
    structure : array of ints, optional
        Structuring element used for the grayscale dilation. `structure`
        may be a non-flat structuring element. The `structure` array applies an
        additive offset for each pixel in the neighborhood.
    output : array, optional
        An array used for storing the output of the dilation may be provided.
    mode : {'reflect','constant','nearest','mirror', 'wrap'}, optional
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
    grey_dilation : ndarray
        Grayscale dilation of `input`.

    See Also
    --------
    binary_dilation, grey_erosion, grey_closing, grey_opening
    generate_binary_structure, maximum_filter

    Notes
    -----
    The grayscale dilation of an image input by a structuring element s defined
    over a domain E is given by:

    (input+s)(x) = max {input(y) + s(x-y), for y in E}

    In particular, for structuring elements defined as
    s(y) = 0 for y in E, the grayscale dilation computes the maximum of the
    input image inside a sliding window defined by E.

    Grayscale dilation [1]_ is a *mathematical morphology* operation [2]_.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Dilation_%28morphology%29
    .. [2] https://en.wikipedia.org/wiki/Mathematical_morphology

    Examples
    --------
    >>> from scipy import ndimage
    >>> import numpy as np
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
    >>> ndimage.grey_dilation(a, size=(3,3))
    array([[0, 0, 0, 0, 0, 0, 0],
           [0, 1, 3, 3, 3, 1, 0],
           [0, 1, 3, 3, 3, 1, 0],
           [0, 1, 3, 3, 3, 2, 0],
           [0, 1, 1, 2, 2, 2, 0],
           [0, 1, 1, 2, 2, 2, 0],
           [0, 0, 0, 0, 0, 0, 0]])
    >>> ndimage.grey_dilation(a, footprint=np.ones((3,3)))
    array([[0, 0, 0, 0, 0, 0, 0],
           [0, 1, 3, 3, 3, 1, 0],
           [0, 1, 3, 3, 3, 1, 0],
           [0, 1, 3, 3, 3, 2, 0],
           [0, 1, 1, 2, 2, 2, 0],
           [0, 1, 1, 2, 2, 2, 0],
           [0, 0, 0, 0, 0, 0, 0]])
    >>> s = ndimage.generate_binary_structure(2,1)
    >>> s
    array([[False,  True, False],
           [ True,  True,  True],
           [False,  True, False]], dtype=bool)
    >>> ndimage.grey_dilation(a, footprint=s)
    array([[0, 0, 0, 0, 0, 0, 0],
           [0, 0, 1, 3, 1, 0, 0],
           [0, 1, 3, 3, 3, 1, 0],
           [0, 1, 1, 3, 2, 1, 0],
           [0, 1, 1, 2, 2, 2, 0],
           [0, 0, 1, 1, 2, 0, 0],
           [0, 0, 0, 0, 0, 0, 0]])
    >>> ndimage.grey_dilation(a, size=(3,3), structure=np.ones((3,3)))
    array([[1, 1, 1, 1, 1, 1, 1],
           [1, 2, 4, 4, 4, 2, 1],
           [1, 2, 4, 4, 4, 2, 1],
           [1, 2, 4, 4, 4, 3, 1],
           [1, 2, 2, 3, 3, 3, 1],
           [1, 2, 2, 3, 3, 3, 1],
           [1, 1, 1, 1, 1, 1, 1]])

    """
    if size is None and footprint is None and structure is None:
        raise ValueError("size, footprint, or structure must be specified")
    if structure is not None:
        structure = np.asarray(structure)
        structure = structure[tuple([slice(None, None, -1)] *
                                    structure.ndim)]
    if footprint is not None:
        footprint = np.asarray(footprint)
        footprint = footprint[tuple([slice(None, None, -1)] *
                                    footprint.ndim)]

    input = np.asarray(input)
    axes = _ni_support._check_axes(axes, input.ndim)
    origin = _ni_support._normalize_sequence(origin, len(axes))
    for ii in range(len(origin)):
        origin[ii] = -origin[ii]
        if footprint is not None:
            sz = footprint.shape[ii]
        elif structure is not None:
            sz = structure.shape[ii]
        elif np.isscalar(size):
            sz = size
        else:
            sz = size[ii]
        if not sz & 1:
            origin[ii] -= 1

    return _filters._min_or_max_filter(input, size, footprint, structure,
                                       output, mode, cval, origin, 0,
                                       axes=axes)

