
def binary_closing(input, structure=None, iterations=1, output=None,
                   origin=0, mask=None, border_value=0, brute_force=False, *,
                   axes=None):
    """
    Multidimensional binary closing with the given structuring element.

    The *closing* of an input image by a structuring element is the
    *erosion* of the *dilation* of the image by the structuring element.

    Parameters
    ----------
    input : array_like
        Binary array_like to be closed. Non-zero (True) elements form
        the subset to be closed.
    structure : array_like, optional
        Structuring element used for the closing. Non-zero elements are
        considered True. If no structuring element is provided an element
        is generated with a square connectivity equal to one (i.e., only
        nearest neighbors are connected to the center, diagonally-connected
        elements are not considered neighbors).
    iterations : int, optional
        The dilation step of the closing, then the erosion step are each
        repeated `iterations` times (one, by default). If iterations is
        less than 1, each operations is repeated until the result does
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
    binary_closing : ndarray of bools
        Closing of the input by the structuring element.

    See Also
    --------
    grey_closing, binary_opening, binary_dilation, binary_erosion,
    generate_binary_structure

    Notes
    -----
    *Closing* [1]_ is a mathematical morphology operation [2]_ that
    consists in the succession of a dilation and an erosion of the
    input with the same structuring element. Closing therefore fills
    holes smaller than the structuring element.

    Together with *opening* (`binary_opening`), closing can be used for
    noise removal.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Closing_%28morphology%29
    .. [2] https://en.wikipedia.org/wiki/Mathematical_morphology

    Examples
    --------
    >>> from scipy import ndimage
    >>> import numpy as np
    >>> a = np.zeros((5,5), dtype=int)
    >>> a[1:-1, 1:-1] = 1; a[2,2] = 0
    >>> a
    array([[0, 0, 0, 0, 0],
           [0, 1, 1, 1, 0],
           [0, 1, 0, 1, 0],
           [0, 1, 1, 1, 0],
           [0, 0, 0, 0, 0]])
    >>> # Closing removes small holes
    >>> ndimage.binary_closing(a).astype(int)
    array([[0, 0, 0, 0, 0],
           [0, 1, 1, 1, 0],
           [0, 1, 1, 1, 0],
           [0, 1, 1, 1, 0],
           [0, 0, 0, 0, 0]])
    >>> # Closing is the erosion of the dilation of the input
    >>> ndimage.binary_dilation(a).astype(int)
    array([[0, 1, 1, 1, 0],
           [1, 1, 1, 1, 1],
           [1, 1, 1, 1, 1],
           [1, 1, 1, 1, 1],
           [0, 1, 1, 1, 0]])
    >>> ndimage.binary_erosion(ndimage.binary_dilation(a)).astype(int)
    array([[0, 0, 0, 0, 0],
           [0, 1, 1, 1, 0],
           [0, 1, 1, 1, 0],
           [0, 1, 1, 1, 0],
           [0, 0, 0, 0, 0]])


    >>> a = np.zeros((7,7), dtype=int)
    >>> a[1:6, 2:5] = 1; a[1:3,3] = 0
    >>> a
    array([[0, 0, 0, 0, 0, 0, 0],
           [0, 0, 1, 0, 1, 0, 0],
           [0, 0, 1, 0, 1, 0, 0],
           [0, 0, 1, 1, 1, 0, 0],
           [0, 0, 1, 1, 1, 0, 0],
           [0, 0, 1, 1, 1, 0, 0],
           [0, 0, 0, 0, 0, 0, 0]])
    >>> # In addition to removing holes, closing can also
    >>> # coarsen boundaries with fine hollows.
    >>> ndimage.binary_closing(a).astype(int)
    array([[0, 0, 0, 0, 0, 0, 0],
           [0, 0, 1, 0, 1, 0, 0],
           [0, 0, 1, 1, 1, 0, 0],
           [0, 0, 1, 1, 1, 0, 0],
           [0, 0, 1, 1, 1, 0, 0],
           [0, 0, 1, 1, 1, 0, 0],
           [0, 0, 0, 0, 0, 0, 0]])
    >>> ndimage.binary_closing(a, structure=np.ones((2,2))).astype(int)
    array([[0, 0, 0, 0, 0, 0, 0],
           [0, 0, 1, 1, 1, 0, 0],
           [0, 0, 1, 1, 1, 0, 0],
           [0, 0, 1, 1, 1, 0, 0],
           [0, 0, 1, 1, 1, 0, 0],
           [0, 0, 1, 1, 1, 0, 0],
           [0, 0, 0, 0, 0, 0, 0]])

    """
    input = np.asarray(input)
    axes = _ni_support._check_axes(axes, input.ndim)
    num_axes = len(axes)
    if structure is None:
        structure = generate_binary_structure(num_axes, 1)

    tmp = binary_dilation(input, structure, iterations, mask, None,
                          border_value, origin, brute_force, axes=axes)
    return binary_erosion(tmp, structure, iterations, mask, output,
                          border_value, origin, brute_force, axes=axes)

