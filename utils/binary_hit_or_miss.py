
def binary_hit_or_miss(input, structure1=None, structure2=None,
                       output=None, origin1=0, origin2=None, *, axes=None):
    """
    Multidimensional binary hit-or-miss transform.

    The hit-or-miss transform finds the locations of a given pattern
    inside the input image.

    Parameters
    ----------
    input : array_like (cast to booleans)
        Binary image where a pattern is to be detected.
    structure1 : array_like (cast to booleans), optional
        Part of the structuring element to be fitted to the foreground
        (non-zero elements) of `input`. If no value is provided, a
        structure of square connectivity 1 is chosen.
    structure2 : array_like (cast to booleans), optional
        Second part of the structuring element that has to miss completely
        the foreground. If no value is provided, the complementary of
        `structure1` is taken.
    output : ndarray, optional
        Array of the same shape as input, into which the output is placed.
        By default, a new array is created.
    origin1 : int or tuple of ints, optional
        Placement of the first part of the structuring element `structure1`,
        by default 0 for a centered structure.
    origin2 : int or tuple of ints, optional
        Placement of the second part of the structuring element `structure2`,
        by default 0 for a centered structure. If a value is provided for
        `origin1` and not for `origin2`, then `origin2` is set to `origin1`.
    axes : tuple of int or None
        The axes over which to apply the filter. If None, `input` is filtered
        along all axes. If `origin1` or `origin2` tuples are provided, their
        length must match the number of axes.

    Returns
    -------
    binary_hit_or_miss : ndarray
        Hit-or-miss transform of `input` with the given structuring
        element (`structure1`, `structure2`).

    See Also
    --------
    binary_erosion

    References
    ----------
    .. [1] https://en.wikipedia.org/wiki/Hit-or-miss_transform

    Examples
    --------
    >>> from scipy import ndimage
    >>> import numpy as np
    >>> a = np.zeros((7,7), dtype=int)
    >>> a[1, 1] = 1; a[2:4, 2:4] = 1; a[4:6, 4:6] = 1
    >>> a
    array([[0, 0, 0, 0, 0, 0, 0],
           [0, 1, 0, 0, 0, 0, 0],
           [0, 0, 1, 1, 0, 0, 0],
           [0, 0, 1, 1, 0, 0, 0],
           [0, 0, 0, 0, 1, 1, 0],
           [0, 0, 0, 0, 1, 1, 0],
           [0, 0, 0, 0, 0, 0, 0]])
    >>> structure1 = np.array([[1, 0, 0], [0, 1, 1], [0, 1, 1]])
    >>> structure1
    array([[1, 0, 0],
           [0, 1, 1],
           [0, 1, 1]])
    >>> # Find the matches of structure1 in the array a
    >>> ndimage.binary_hit_or_miss(a, structure1=structure1).astype(int)
    array([[0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0],
           [0, 0, 1, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 1, 0, 0],
           [0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0]])
    >>> # Change the origin of the filter
    >>> # origin1=1 is equivalent to origin1=(1,1) here
    >>> ndimage.binary_hit_or_miss(a, structure1=structure1,\\
    ... origin1=1).astype(int)
    array([[0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 1, 0, 0, 0],
           [0, 0, 0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0, 1, 0],
           [0, 0, 0, 0, 0, 0, 0]])

    """
    input = np.asarray(input)
    axes = _ni_support._check_axes(axes, input.ndim)
    num_axes = len(axes)
    if structure1 is None:
        structure1 = generate_binary_structure(num_axes, 1)
    else:
        structure1 = np.asarray(structure1)
    if structure2 is None:
        structure2 = np.logical_not(structure1)
    origin1 = _ni_support._normalize_sequence(origin1, num_axes)
    if origin2 is None:
        origin2 = origin1
    else:
        origin2 = _ni_support._normalize_sequence(origin2, num_axes)

    tmp1 = _binary_erosion(input, structure1, 1, None, None, 0, origin1,
                           0, False, axes)
    inplace = isinstance(output, np.ndarray)
    result = _binary_erosion(input, structure2, 1, None, output, 0,
                             origin2, 1, False, axes)
    if inplace:
        np.logical_not(output, output)
        np.logical_and(tmp1, output, output)
    else:
        np.logical_not(result, result)
        return np.logical_and(tmp1, result)

