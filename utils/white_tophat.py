
def white_tophat(input, size=None, footprint=None, structure=None,
                 output=None, mode="reflect", cval=0.0, origin=0, *,
                 axes=None):
    """
    Multidimensional white tophat filter.

    Parameters
    ----------
    input : array_like
        Input.
    size : tuple of ints
        Shape of a flat and full structuring element used for the filter.
        Optional if `footprint` or `structure` is provided.
    footprint : array of ints, optional
        Positions of elements of a flat structuring element
        used for the white tophat filter.
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
        Value to fill past edges of input if `mode` is 'constant'.
        Default is 0.0.
    origin : scalar, optional
        The `origin` parameter controls the placement of the filter.
        Default is 0.
    axes : tuple of int or None
        The axes over which to apply the filter. If None, `input` is filtered
        along all axes. If an `origin` tuple is provided, its length must match
        the number of axes.

    Returns
    -------
    output : ndarray
        Result of the filter of `input` with `structure`.

    See Also
    --------
    black_tophat

    Examples
    --------
    Subtract gray background from a bright peak.

    >>> from scipy.ndimage import generate_binary_structure, white_tophat
    >>> import numpy as np
    >>> square = generate_binary_structure(rank=2, connectivity=3)
    >>> bright_on_gray = np.array([[2, 3, 3, 3, 2],
    ...                            [3, 4, 5, 4, 3],
    ...                            [3, 5, 9, 5, 3],
    ...                            [3, 4, 5, 4, 3],
    ...                            [2, 3, 3, 3, 2]])
    >>> white_tophat(input=bright_on_gray, structure=square)
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
    tmp = grey_erosion(input, size, footprint, structure, None, mode,
                       cval, origin, axes=axes)
    tmp = grey_dilation(tmp, size, footprint, structure, output, mode,
                        cval, origin, axes=axes)
    if tmp is None:
        tmp = output

    if input.dtype == np.bool_ and tmp.dtype == np.bool_:
        np.bitwise_xor(input, tmp, out=tmp)
    else:
        np.subtract(input, tmp, out=tmp)
    return tmp

