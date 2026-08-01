
def binary_erosion(input, structure=None, iterations=1, mask=None, output=None,
                   border_value=0, origin=0, brute_force=False, *, axes=None):
    """
    Multidimensional binary erosion with a given structuring element.

    Binary erosion is a mathematical morphology operation used for image
    processing.

    Parameters
    ----------
    input : array_like
        Binary image to be eroded. Non-zero (True) elements form
        the subset to be eroded.
    structure : array_like, optional
        Structuring element used for the erosion. Non-zero elements are
        considered True. If no structuring element is provided, an element
        is generated with a square connectivity equal to one.
    iterations : int, optional
        The erosion is repeated `iterations` times (one, by default).
        If iterations is less than 1, the erosion is repeated until the
        result does not change anymore.
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
        the last iteration are tracked as candidates to be updated (eroded) in
        the current iteration; if True all pixels are considered as candidates
        for erosion, regardless of what happened in the previous iteration.
        False by default.
    axes : tuple of int or None
        The axes over which to apply the filter. If None, `input` is filtered
        along all axes. If an `origin` tuple is provided, its length must match
        the number of axes.

    Returns
    -------
    binary_erosion : ndarray of bools
        Erosion of the input by the structuring element.

    See Also
    --------
    grey_erosion, binary_dilation, binary_closing, binary_opening,
    generate_binary_structure

    Notes
    -----
    Erosion [1]_ is a mathematical morphology operation [2]_ that uses a
    structuring element for shrinking the shapes in an image. The binary
    erosion of an image by a structuring element is the locus of the points
    where a superimposition of the structuring element centered on the point
    is entirely contained in the set of non-zero elements of the image.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Erosion_%28morphology%29
    .. [2] https://en.wikipedia.org/wiki/Mathematical_morphology

    Examples
    --------
    >>> from scipy import ndimage
    >>> import numpy as np
    >>> a = np.zeros((7,7), dtype=int)
    >>> a[1:6, 2:5] = 1
    >>> a
    array([[0, 0, 0, 0, 0, 0, 0],
           [0, 0, 1, 1, 1, 0, 0],
           [0, 0, 1, 1, 1, 0, 0],
           [0, 0, 1, 1, 1, 0, 0],
           [0, 0, 1, 1, 1, 0, 0],
           [0, 0, 1, 1, 1, 0, 0],
           [0, 0, 0, 0, 0, 0, 0]])
    >>> ndimage.binary_erosion(a).astype(a.dtype)
    array([[0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 1, 0, 0, 0],
           [0, 0, 0, 1, 0, 0, 0],
           [0, 0, 0, 1, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0]])
    >>> #Erosion removes objects smaller than the structure
    >>> ndimage.binary_erosion(a, structure=np.ones((5,5))).astype(a.dtype)
    array([[0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0]])

    """
    return _binary_erosion(input, structure, iterations, mask,
                           output, border_value, origin, 0, brute_force, axes)

