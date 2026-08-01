
def grey_closing(input, size=None, footprint=None, structure=None,
                 output=None, mode="reflect", cval=0.0, origin=0, *,
                 axes=None):
    """
    Multidimensional grayscale closing.

    A grayscale closing consists in the succession of a grayscale dilation,
    and a grayscale erosion.

    Parameters
    ----------
    input : array_like
        Array over which the grayscale closing is to be computed.
    size : tuple of ints
        Shape of a flat and full structuring element used for the grayscale
        closing. Optional if `footprint` or `structure` is provided.
    footprint : array of ints, optional
        Positions of non-infinite elements of a flat structuring element
        used for the grayscale closing.
    structure : array of ints, optional
        Structuring element used for the grayscale closing. `structure`
        may be a non-flat structuring element. The `structure` array applies
        offsets to the pixels in a neighborhood (the offset is additive during
        dilation and subtractive during erosion)
    output : array, optional
        An array used for storing the output of the closing may be provided.
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
    grey_closing : ndarray
        Result of the grayscale closing of `input` with `structure`.

    See Also
    --------
    binary_closing, grey_dilation, grey_erosion, grey_opening,
    generate_binary_structure

    Notes
    -----
    The action of a grayscale closing with a flat structuring element amounts
    to smoothen deep local minima, whereas binary closing fills small holes.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Mathematical_morphology

    Examples
    --------
    >>> from scipy import ndimage
    >>> import numpy as np
    >>> a = np.arange(36).reshape((6,6))
    >>> a[3,3] = 0
    >>> a
    array([[ 0,  1,  2,  3,  4,  5],
           [ 6,  7,  8,  9, 10, 11],
           [12, 13, 14, 15, 16, 17],
           [18, 19, 20,  0, 22, 23],
           [24, 25, 26, 27, 28, 29],
           [30, 31, 32, 33, 34, 35]])
    >>> ndimage.grey_closing(a, size=(3,3))
    array([[ 7,  7,  8,  9, 10, 11],
           [ 7,  7,  8,  9, 10, 11],
           [13, 13, 14, 15, 16, 17],
           [19, 19, 20, 20, 22, 23],
           [25, 25, 26, 27, 28, 29],
           [31, 31, 32, 33, 34, 35]])
    >>> # Note that the local minimum a[3,3] has disappeared

    """
    if (size is not None) and (footprint is not None):
        warnings.warn("ignoring size because footprint is set",
                      UserWarning, stacklevel=2)
    tmp = grey_dilation(input, size, footprint, structure, None, mode,
                        cval, origin, axes=axes)
    return grey_erosion(tmp, size, footprint, structure, output, mode,
                        cval, origin, axes=axes)

