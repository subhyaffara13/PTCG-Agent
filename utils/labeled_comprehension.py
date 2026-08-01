
def labeled_comprehension(input, labels, index, func, out_dtype, default,
                          pass_positions=False):
    """
    Roughly equivalent to [func(input[labels == i]) for i in index].

    Sequentially applies an arbitrary function (that works on array_like input)
    to subsets of an N-D image array specified by `labels` and `index`.
    The option exists to provide the function with positional parameters as the
    second argument.

    Parameters
    ----------
    input : array_like
        Data from which to select `labels` to process.
    labels : array_like or None
        Labels to objects in `input`.
        If not None, array must be same shape as `input`.
        If None, `func` is applied to raveled `input`.
    index : int, sequence of ints or None
        Subset of `labels` to which to apply `func`.
        If a scalar, a single value is returned.
        If None, `func` is applied to all non-zero values of `labels`.
    func : callable
        Python function to apply to `labels` from `input`.
    out_dtype : dtype
        Dtype to use for `result`.
    default : int, float or None
        Default return value when an element of `index` does not exist
        in `labels`.
    pass_positions : bool, optional
        If True, pass linear indices to `func` as a second argument.
        Default is False.

    Returns
    -------
    result : ndarray
        Result of applying `func` to each of `labels` to `input` in `index`.

    Examples
    --------
    >>> import numpy as np
    >>> a = np.array([[1, 2, 0, 0],
    ...               [5, 3, 0, 4],
    ...               [0, 0, 0, 7],
    ...               [9, 3, 0, 0]])
    >>> from scipy import ndimage
    >>> lbl, nlbl = ndimage.label(a)
    >>> lbls = np.arange(1, nlbl+1)
    >>> ndimage.labeled_comprehension(a, lbl, lbls, np.mean, float, 0)
    array([ 2.75,  5.5 ,  6.  ])

    Falling back to `default`:

    >>> lbls = np.arange(1, nlbl+2)
    >>> ndimage.labeled_comprehension(a, lbl, lbls, np.mean, float, -1)
    array([ 2.75,  5.5 ,  6.  , -1.  ])

    Passing positions:

    >>> def fn(val, pos):
    ...     print("fn says: %s : %s" % (val, pos))
    ...     return (val.sum()) if (pos.sum() % 2 == 0) else (-val.sum())
    ...
    >>> ndimage.labeled_comprehension(a, lbl, lbls, fn, float, 0, True)
    fn says: [1 2 5 3] : [0 1 4 5]
    fn says: [4 7] : [ 7 11]
    fn says: [9 3] : [12 13]
    array([ 11.,  11., -12.,   0.])

    """

    as_scalar = np.isscalar(index)
    input = np.asarray(input)

    if pass_positions:
        positions = np.arange(input.size).reshape(input.shape)

    if labels is None:
        if index is not None:
            raise ValueError("index without defined labels")
        if not pass_positions:
            return func(input.ravel())
        else:
            return func(input.ravel(), positions.ravel())

    labels = np.asarray(labels)

    try:
        input, labels = np.broadcast_arrays(input, labels)
    except ValueError as e:
        raise ValueError("input and labels must have the same shape "
                            "(excepting dimensions with width 1)") from e

    if index is None:
        if not pass_positions:
            return func(input[labels > 0])
        else:
            return func(input[labels > 0], positions[labels > 0])

    index = np.atleast_1d(index)
    if np.any(index.astype(labels.dtype).astype(index.dtype) != index):
        raise ValueError(f"Cannot convert index values from <{index.dtype}> to "
                         f"<{labels.dtype}> (labels' type) without loss of precision")

    index = index.astype(labels.dtype)

    # optimization: find min/max in index,
    # and select those parts of labels, input, and positions
    lo = index.min()
    hi = index.max()
    mask = (labels >= lo) & (labels <= hi)

    # this also ravels the arrays
    labels = labels[mask]
    input = input[mask]
    if pass_positions:
        positions = positions[mask]

    # sort everything by labels
    label_order = labels.argsort()
    labels = labels[label_order]
    input = input[label_order]
    if pass_positions:
        positions = positions[label_order]

    index_order = index.argsort()
    sorted_index = index[index_order]

    def do_map(inputs, output):
        """labels must be sorted"""
        nidx = sorted_index.size

        # Find boundaries for each stretch of constant labels
        # This could be faster, but we already paid N log N to sort labels.
        lo = np.searchsorted(labels, sorted_index, side='left')
        hi = np.searchsorted(labels, sorted_index, side='right')

        for i, l, h in zip(range(nidx), lo, hi):
            if l == h:
                continue
            output[i] = func(*[inp[l:h] for inp in inputs])

    temp = np.empty(index.shape, out_dtype)
    temp[:] = default
    if not pass_positions:
        do_map([input], temp)
    else:
        do_map([input, positions], temp)

    output = np.zeros(index.shape, out_dtype)
    output[index_order] = temp
    if as_scalar:
        output = output[0]

    return output

