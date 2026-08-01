
def binary_propagation(input, structure=None, mask=None,
                       output=None, border_value=0, origin=0, *, axes=None):
    """
    Multidimensional binary propagation with the given structuring element.

    Parameters
    ----------
    input : array_like
        Binary image to be propagated inside `mask`.
    structure : array_like, optional
        Structuring element used in the successive dilations. The output
        may depend on the structuring element, especially if `mask` has
        several connex components. If no structuring element is
        provided, an element is generated with a squared connectivity equal
        to one.
    mask : array_like, optional
        Binary mask defining the region into which `input` is allowed to
        propagate.
    output : ndarray, optional
        Array of the same shape as input, into which the output is placed.
        By default, a new array is created.
    border_value : int (cast to 0 or 1), optional
        Value at the border in the output array.
    origin : int or tuple of ints, optional
        Placement of the filter, by default 0.
    axes : tuple of int or None
        The axes over which to apply the filter. If None, `input` is filtered
        along all axes. If an `origin` tuple is provided, its length must match
        the number of axes.

    Returns
    -------
    binary_propagation : ndarray
        Binary propagation of `input` inside `mask`.

    Notes
    -----
    This function is functionally equivalent to calling binary_dilation
    with the number of iterations less than one: iterative dilation until
    the result does not change anymore.

    The succession of an erosion and propagation inside the original image
    can be used instead of an *opening* for deleting small objects while
    keeping the contours of larger objects untouched.

    References
    ----------
    .. [1] http://cmm.ensmp.fr/~serra/cours/pdf/en/ch6en.pdf, slide 15.
    .. [2] I.T. Young, J.J. Gerbrands, and L.J. van Vliet, "Fundamentals of
        image processing", 1998
        ftp://qiftp.tudelft.nl/DIPimage/docs/FIP2.3.pdf

    Examples
    --------
    >>> from scipy import ndimage
    >>> import numpy as np
    >>> input = np.zeros((8, 8), dtype=int)
    >>> input[2, 2] = 1
    >>> mask = np.zeros((8, 8), dtype=int)
    >>> mask[1:4, 1:4] = mask[4, 4]  = mask[6:8, 6:8] = 1
    >>> input
    array([[0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 1, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0]])
    >>> mask
    array([[0, 0, 0, 0, 0, 0, 0, 0],
           [0, 1, 1, 1, 0, 0, 0, 0],
           [0, 1, 1, 1, 0, 0, 0, 0],
           [0, 1, 1, 1, 0, 0, 0, 0],
           [0, 0, 0, 0, 1, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 1, 1],
           [0, 0, 0, 0, 0, 0, 1, 1]])
    >>> ndimage.binary_propagation(input, mask=mask).astype(int)
    array([[0, 0, 0, 0, 0, 0, 0, 0],
           [0, 1, 1, 1, 0, 0, 0, 0],
           [0, 1, 1, 1, 0, 0, 0, 0],
           [0, 1, 1, 1, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0]])
    >>> ndimage.binary_propagation(input, mask=mask,\\
    ... structure=np.ones((3,3))).astype(int)
    array([[0, 0, 0, 0, 0, 0, 0, 0],
           [0, 1, 1, 1, 0, 0, 0, 0],
           [0, 1, 1, 1, 0, 0, 0, 0],
           [0, 1, 1, 1, 0, 0, 0, 0],
           [0, 0, 0, 0, 1, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0, 0]])

    >>> # Comparison between opening and erosion+propagation
    >>> a = np.zeros((6,6), dtype=int)
    >>> a[2:5, 2:5] = 1; a[0, 0] = 1; a[5, 5] = 1
    >>> a
    array([[1, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0],
           [0, 0, 1, 1, 1, 0],
           [0, 0, 1, 1, 1, 0],
           [0, 0, 1, 1, 1, 0],
           [0, 0, 0, 0, 0, 1]])
    >>> ndimage.binary_opening(a).astype(int)
    array([[0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0],
           [0, 0, 0, 1, 0, 0],
           [0, 0, 1, 1, 1, 0],
           [0, 0, 0, 1, 0, 0],
           [0, 0, 0, 0, 0, 0]])
    >>> b = ndimage.binary_erosion(a)
    >>> b.astype(int)
    array([[0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0],
           [0, 0, 0, 1, 0, 0],
           [0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0]])
    >>> ndimage.binary_propagation(b, mask=a).astype(int)
    array([[0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0],
           [0, 0, 1, 1, 1, 0],
           [0, 0, 1, 1, 1, 0],
           [0, 0, 1, 1, 1, 0],
           [0, 0, 0, 0, 0, 0]])

    """
    return binary_dilation(input, structure, -1, mask, output,
                           border_value, origin, axes=axes)

