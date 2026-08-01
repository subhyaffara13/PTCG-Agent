
def grey_erosion(input, size=None, footprint=None, structure=None,
                 output=None, mode="reflect", cval=0.0, origin=0, *,
                 axes=None):
    """
    Calculate a greyscale erosion, using either a structuring element,
    or a footprint corresponding to a flat structuring element.

    Grayscale erosion is a mathematical morphology operation. For the
    simple case of a full and flat structuring element, it can be viewed
    as a minimum filter over a sliding window.

    Parameters
    ----------
    input : array_like
        Array over which the grayscale erosion is to be computed.
    size : tuple of ints
        Shape of a flat and full structuring element used for the grayscale
        erosion. Optional if `footprint` or `structure` is provided.
    footprint : array of ints, optional
        Positions of non-infinite elements of a flat structuring element
        used for the grayscale erosion. Non-zero values give the set of
        neighbors of the center over which the minimum is chosen.
    structure : array of ints, optional
        Structuring element used for the grayscale erosion. `structure`
        may be a non-flat structuring element. The `structure` array applies a
        subtractive offset for each pixel in the neighborhood.
    output : array, optional
        An array used for storing the output of the erosion may be provided.
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
    output : ndarray
        Grayscale erosion of `input`.

    See Also
    --------
    binary_erosion, grey_dilation, grey_opening, grey_closing
    generate_binary_structure, minimum_filter

    Notes
    -----
    The grayscale erosion of an image input by a structuring element s defined
    over a domain E is given by:

    (input+s)(x) = min {input(y) - s(x-y), for y in E}

    In particular, for structuring elements defined as
    s(y) = 0 for y in E, the grayscale erosion computes the minimum of the
    input image inside a sliding window defined by E.

    Grayscale erosion [1]_ is a *mathematical morphology* operation [2]_.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Erosion_%28morphology%29
    .. [2] https://en.wikipedia.org/wiki/Mathematical_morphology

    Examples
    --------
    >>> from scipy import ndimage
    >>> import numpy as np
    >>> a = np.zeros((7,7), dtype=int)
    >>> a[1:6, 1:6] = 3
    >>> a[4,4] = 2; a[2,3] = 1
    >>> a
    array([[0, 0, 0, 0, 0, 0, 0],
           [0, 3, 3, 3, 3, 3, 0],
           [0, 3, 3, 1, 3, 3, 0],
           [0, 3, 3, 3, 3, 3, 0],
           [0, 3, 3, 3, 2, 3, 0],
           [0, 3, 3, 3, 3, 3, 0],
           [0, 0, 0, 0, 0, 0, 0]])
    >>> ndimage.grey_erosion(a, size=(3,3))
    array([[0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0],
           [0, 0, 1, 1, 1, 0, 0],
           [0, 0, 1, 1, 1, 0, 0],
           [0, 0, 3, 2, 2, 0, 0],
           [0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0]])
    >>> footprint = ndimage.generate_binary_structure(2, 1)
    >>> footprint
    array([[False,  True, False],
           [ True,  True,  True],
           [False,  True, False]], dtype=bool)
    >>> # Diagonally-connected elements are not considered neighbors
    >>> ndimage.grey_erosion(a, footprint=footprint)
    array([[0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0],
           [0, 0, 1, 1, 1, 0, 0],
           [0, 0, 3, 1, 2, 0, 0],
           [0, 0, 3, 2, 2, 0, 0],
           [0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0]])

    """
    if size is None and footprint is None and structure is None:
        raise ValueError("size, footprint, or structure must be specified")

    return _filters._min_or_max_filter(input, size, footprint, structure,
                                       output, mode, cval, origin, 1,
                                       axes=axes)

