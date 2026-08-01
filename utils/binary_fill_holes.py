
def binary_fill_holes(input, structure=None, output=None, origin=0, *,
                      axes=None):
    """
    Fill the holes in binary objects.


    Parameters
    ----------
    input : array_like
        N-D binary array with holes to be filled
    structure : array_like, optional
        Structuring element used in the computation; large-size elements
        make computations faster but may miss holes separated from the
        background by thin regions. The default element (with a square
        connectivity equal to one) yields the intuitive result where all
        holes in the input have been filled.
    output : ndarray, optional
        Array of the same shape as input, into which the output is placed.
        By default, a new array is created.
    origin : int, tuple of ints, optional
        Position of the structuring element.
    axes : tuple of int or None
        The axes over which to apply the filter. If None, `input` is filtered
        along all axes. If an `origin` tuple is provided, its length must match
        the number of axes.

    Returns
    -------
    out : ndarray
        Transformation of the initial image `input` where holes have been
        filled.

    See Also
    --------
    binary_dilation, binary_propagation, label

    Notes
    -----
    The algorithm used in this function consists in invading the complementary
    of the shapes in `input` from the outer boundary of the image,
    using binary dilations. Holes are not connected to the boundary and are
    therefore not invaded. The result is the complementary subset of the
    invaded region.

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Mathematical_morphology


    Examples
    --------
    >>> from scipy import ndimage
    >>> import numpy as np
    >>> a = np.zeros((5, 5), dtype=int)
    >>> a[1:4, 1:4] = 1
    >>> a[2,2] = 0
    >>> a
    array([[0, 0, 0, 0, 0],
           [0, 1, 1, 1, 0],
           [0, 1, 0, 1, 0],
           [0, 1, 1, 1, 0],
           [0, 0, 0, 0, 0]])
    >>> ndimage.binary_fill_holes(a).astype(int)
    array([[0, 0, 0, 0, 0],
           [0, 1, 1, 1, 0],
           [0, 1, 1, 1, 0],
           [0, 1, 1, 1, 0],
           [0, 0, 0, 0, 0]])
    >>> # Too big structuring element
    >>> ndimage.binary_fill_holes(a, structure=np.ones((5,5))).astype(int)
    array([[0, 0, 0, 0, 0],
           [0, 1, 1, 1, 0],
           [0, 1, 0, 1, 0],
           [0, 1, 1, 1, 0],
           [0, 0, 0, 0, 0]])

    """
    input = np.asarray(input)
    mask = np.logical_not(input)
    tmp = np.zeros(mask.shape, bool)
    inplace = isinstance(output, np.ndarray)
    if inplace:
        binary_dilation(tmp, structure, -1, mask, output, 1, origin, axes=axes)
        np.logical_not(output, output)
    else:
        output = binary_dilation(tmp, structure, -1, mask, None, 1,
                                 origin, axes=axes)
        np.logical_not(output, output)
        return output

