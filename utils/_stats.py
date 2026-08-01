
def _stats(input, labels=None, index=None, centered=False):
    """Count, sum, and optionally compute (sum - centre)^2 of input by label

    Parameters
    ----------
    input : array_like, N-D
        The input data to be analyzed.
    labels : array_like (N-D), optional
        The labels of the data in `input`. This array must be broadcast
        compatible with `input`; typically, it is the same shape as `input`.
        If `labels` is None, all nonzero values in `input` are treated as
        the single labeled group.
    index : label or sequence of labels, optional
        These are the labels of the groups for which the stats are computed.
        If `index` is None, the stats are computed for the single group where
        `labels` is greater than 0.
    centered : bool, optional
        If True, the centered sum of squares for each labeled group is
        also returned. Default is False.

    Returns
    -------
    counts : int or ndarray of ints
        The number of elements in each labeled group.
    sums : scalar or ndarray of scalars
        The sums of the values in each labeled group.
    sums_c : scalar or ndarray of scalars, optional
        The sums of mean-centered squares of the values in each labeled group.
        This is only returned if `centered` is True.

    """
    def single_group(vals):
        if centered:
            vals_c = vals - vals.mean()
            return vals.size, vals.sum(), (vals_c * vals_c.conjugate()).sum()
        else:
            return vals.size, vals.sum()

    input = np.asarray(input)
    if labels is None:
        return single_group(input)

    labels = np.asarray(labels)
    # ensure input and labels match sizes
    input, labels = np.broadcast_arrays(input, labels)

    if index is None:
        return single_group(input[labels > 0])

    if np.isscalar(index):
        return single_group(input[labels == index])

    def _sum_centered(labels):
        # `labels` is expected to be an ndarray with the same shape as `input`.
        # It must contain the label indices (which are not necessarily the labels
        # themselves).
        means = sums / counts
        centered_input = input - means[labels]
        # bincount expects 1-D inputs, so we ravel the arguments.
        bc = np.bincount(labels.ravel(),
                              weights=(centered_input *
                                       centered_input.conjugate()).ravel())
        return bc

    # Remap labels to unique integers if necessary, or if the largest
    # label is larger than the number of values.

    if (not _safely_castable_to_int(labels.dtype) or
            labels.min() < 0 or labels.max() > labels.size):
        # Use np.unique to generate the label indices.  `new_labels` will
        # be 1-D, but it should be interpreted as the flattened N-D array of
        # label indices.
        unique_labels, new_labels = np.unique(labels, return_inverse=True)
        new_labels = np.reshape(new_labels, (-1,))  # flatten, since it may be >1-D
        counts = np.bincount(new_labels)
        sums = np.bincount(new_labels, weights=input.ravel())
        if centered:
            # Compute the sum of the mean-centered squares.
            # We must reshape new_labels to the N-D shape of `input` before
            # passing it _sum_centered.
            sums_c = _sum_centered(new_labels.reshape(labels.shape))
        idxs = np.searchsorted(unique_labels, index)
        # make all of idxs valid
        idxs[idxs >= unique_labels.size] = 0
        found = (unique_labels[idxs] == index)
    else:
        # labels are an integer type allowed by bincount, and there aren't too
        # many, so call bincount directly.
        counts = np.bincount(labels.ravel())
        sums = np.bincount(labels.ravel(), weights=input.ravel())
        if centered:
            sums_c = _sum_centered(labels)
        # make sure all index values are valid
        idxs = np.asanyarray(index, np.int_).copy()
        found = (idxs >= 0) & (idxs < counts.size)
        idxs[~found] = 0

    counts = counts[idxs]
    counts[~found] = 0
    sums = sums[idxs]
    sums[~found] = 0

    if not centered:
        return (counts, sums)
    else:
        sums_c = sums_c[idxs]
        sums_c[~found] = 0
        return (counts, sums, sums_c)

