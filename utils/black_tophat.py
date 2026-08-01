
def black_tophat(input, size=None, footprint=None, structure=None, output=None,
                 mode="reflect", cval=0.0, origin=0, *, axes=None):
    """
    Multidimensional black tophat filter.

    Parameters
    ----------
    input : array_like
        Input.
    size : tuple of ints, optional
        Shape of a flat and full structuring element used for the filter.
        Optional if `footprint` or `structure` is provided.
    footprint : array of ints, optional
        Positions of non-infinite elements of a flat structuring element
        used for the black tophat filter.
    structure : array of ints, optional
        Structuring element used for the filter. `structure` may be a non-flat
        structuring element. The `structure` array applies offsets to the
        pixels in a neighborhood (the offset is additive during dilation and
        subtractive during erosion)
    output : array, optional
        An array used for storing the output of the filter may be provided.
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
    black_tophat : ndarray
        Result of the filter of `input` with `structure`.

    See Also
    --------
    white_tophat, grey_opening, grey_closing

    Examples
    --------
    Change dark peak to bright peak and subtract background.

    >>> from scipy.ndimage import generate_binary_structure, black_tophat
    >>> import numpy as np
    >>> square = generate_binary_structure(rank=2, connectivity=3)
    >>> dark_on_gray = np.array([[7, 6, 6, 6, 7],
    ...                          [6, 5, 4, 5, 6],
    ...                          [6, 4, 0, 4, 6],
    ...                          [6, 5, 4, 5, 6],
    ...                          [7, 6, 6, 6, 7]])
    >>> black_tophat(input=dark_on_gray, structure=square)
    array([[0, 0, 0, 0, 0],
           [0, 0, 1, 0, 0],
           [0, 1, 5, 1, 0],
           [0, 0, 1, 0, 0],
           [0, 0, 0, 0, 0]])

    """
    input = np.asarray(input)

    if (size is not None) and (footprint is not None):
        warnings.warn("ignoring size because footprint is set",
                      UserWarning, stacklevel=2)
    tmp = grey_dilation(input, size, footprint, structure, None, mode,
                        cval, origin, axes=axes)
    tmp = grey_erosion(tmp, size, footprint, structure, output, mode,
                       cval, origin, axes=axes)
    if tmp is None:
        tmp = output

    if input.dtype == np.bool_ and tmp.dtype == np.bool_:
        np.bitwise_xor(tmp, input, out=tmp)
    else:
        np.subtract(tmp, input, out=tmp)
    return tmp

