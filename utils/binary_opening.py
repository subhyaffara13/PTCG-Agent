
def binary_opening(input, structure=None, iterations=1, output=None,
                   origin=0, mask=None, border_value=0, brute_force=False, *,
                   axes=None):
    """
    Multidimensional binary opening with the given structuring element.

    The *opening* of an input image by a structuring element is the
    *dilation* of the *erosion* of the image by the structuring element.

    Parameters
    ----------
    input : array_like
        Binary array_like to be opened. Non-zero (True) elements form
        the subset to be opened.
    structure : array_like, optional
        Structuring element used for the opening. Non-zero elements are
        considered True. If no structuring element is provided an element
        is generated with a square connectivity equal to one (i.e., only
        nearest neighbors are connected to the center, diagonally-connected
        elements are not considered neighbors).
    iterations : int, optional
        The erosion step of the opening, then the dilation step are each
        repeated `iterations` times (one, by default). If `iterations` is
        less than 1, each operation is repeated until the result does
        not change anymore. Only an integer of iterations is accepted.
    output : ndarray, optional
        Array of the same shape as input, into which the output is placed.
        By default, a new array is created.
    origin : int or tuple of ints, optional
        Placement of the filter, by default 0.
    mask : array_like, optional
        If a mask is given, only those elements with a True value at
        the corresponding mask element are modified at each iteration.

        .. versionadded:: 1.1.0
    border_value : int (cast to 0 or 1), optional
        Value at the border in the output array.

        .. versionadded:: 1.1.0
    brute_force : bool, optional
        Memory condition: if False, only the pixels whose value was changed in
        the last iteration are tracked as candidates to be updated in the
        current iteration; if True all pixels are considered as candidates for
        update, regardless of what happened in the previous iteration.
        False by default.

        .. versionadded:: 1.1.0
    axes : tuple of int or None
        The axes over which to apply the filter. If None, `input` is filtered
        along all axes. If an `origin` tuple is provided, its length must match
        the number of axes.

    Returns
    -------
    binary_opening : ndarray of bools
        Opening of the input by the structuring element.

    See Also
    --------
    grey_opening, binary_closing, binary_erosion, binary_dilation,
    generate_binary_structure

    Notes
    -----
    *Opening* [1]_ is a mathematical morphology operation [2]_ that
    consists in the succession of an erosion and a dilation of the
    input with the same structuring element. Opening, therefore, removes
    objects smaller than the structuring element.

    Together with *closing* (`binary_closing`), opening can be used for
    noise removal.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Opening_%28morphology%29
    .. [2] https://en.wikipedia.org/wiki/Mathematical_morphology

    Examples
    --------
    >>> from scipy import ndimage
    >>> import numpy as np
    >>> a = np.zeros((5,5), dtype=int)
    >>> a[1:4, 1:4] = 1; a[4, 4] = 1
    >>> a
    array([[0, 0, 0, 0, 0],
           [0, 1, 1, 1, 0],
           [0, 1, 1, 1, 0],
           [0, 1, 1, 1, 0],
           [0, 0, 0, 0, 1]])
    >>> # Opening removes small objects
    >>> ndimage.binary_opening(a, structure=np.ones((3,3))).astype(int)
    array([[0, 0, 0, 0, 0],
           [0, 1, 1, 1, 0],
           [0, 1, 1, 1, 0],
           [0, 1, 1, 1, 0],
           [0, 0, 0, 0, 0]])
    >>> # Opening can also smooth corners
    >>> ndimage.binary_opening(a).astype(int)
    array([[0, 0, 0, 0, 0],
           [0, 0, 1, 0, 0],
           [0, 1, 1, 1, 0],
           [0, 0, 1, 0, 0],
           [0, 0, 0, 0, 0]])
    >>> # Opening is the dilation of the erosion of the input
    >>> ndimage.binary_erosion(a).astype(int)
    array([[0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 1, 0, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0]])
    >>> ndimage.binary_dilation(ndimage.binary_erosion(a)).astype(int)
    array([[0, 0, 0, 0, 0],
           [0, 0, 1, 0, 0],
           [0, 1, 1, 1, 0],
           [0, 0, 1, 0, 0],
           [0, 0, 0, 0, 0]])

    """
    input = np.asarray(input)
    axes = _ni_support._check_axes(axes, input.ndim)
    num_axes = len(axes)
    if structure is None:
        structure = generate_binary_structure(num_axes, 1)

    tmp = binary_erosion(input, structure, iterations, mask, None,
                         border_value, origin, brute_force, axes=axes)
    return binary_dilation(tmp, structure, iterations, mask, output,
                           border_value, origin, brute_force, axes=axes)

