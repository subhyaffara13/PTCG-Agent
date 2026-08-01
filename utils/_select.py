
def _select(input, labels=None, index=None, find_min=False, find_max=False,
            find_min_positions=False, find_max_positions=False,
            find_median=False):
    """Returns min, max, or both, plus their positions (if requested), and
    median."""

    input = np.asanyarray(input)

    find_positions = find_min_positions or find_max_positions
    positions = None
    if find_positions:
        positions = np.arange(input.size).reshape(input.shape)

    def single_group(vals, positions):
        result = []
        if find_min:
            result += [vals.min()]
        if find_min_positions:
            result += [positions[vals == vals.min()][0]]
        if find_max:
            result += [vals.max()]
        if find_max_positions:
            result += [positions[vals == vals.max()][0]]
        if find_median:
            result += [np.median(vals)]
        return result

    if labels is None:
        return single_group(input, positions)

    labels = np.asarray(labels)
    # ensure input and labels match sizes
    input, labels = np.broadcast_arrays(input, labels)

    if index is None:
        mask = (labels > 0)
        masked_positions = None
        if find_positions:
            masked_positions = positions[mask]
        return single_group(input[mask], masked_positions)

    if np.isscalar(index):
        mask = (labels == index)
        masked_positions = None
        if find_positions:
            masked_positions = positions[mask]
        return single_group(input[mask], masked_positions)

    index = np.asarray(index)

    # remap labels to unique integers if necessary, or if the largest
    # label is larger than the number of values.
    if (not _safely_castable_to_int(labels.dtype) or
            labels.min() < 0 or labels.max() > labels.size):
        # remap labels, and indexes
        unique_labels, labels = np.unique(labels, return_inverse=True)
        idxs = np.searchsorted(unique_labels, index)

        # make all of idxs valid
        idxs[idxs >= unique_labels.size] = 0
        found = (unique_labels[idxs] == index)
    else:
        # labels are an integer type, and there aren't too many
        idxs = np.asanyarray(index, np.int_).copy()
        found = (idxs >= 0) & (idxs <= labels.max())

    idxs[~ found] = labels.max() + 1

    if find_median:
        order = np.lexsort((input.ravel(), labels.ravel()))
    else:
        order = input.ravel().argsort()
    input = input.ravel()[order]
    labels = labels.ravel()[order]
    if find_positions:
        positions = positions.ravel()[order]

    result = []
    if find_min:
        mins = np.zeros(labels.max() + 2, input.dtype)
        mins[labels[::-1]] = input[::-1]
        result += [mins[idxs]]
    if find_min_positions:
        minpos = np.zeros(labels.max() + 2, int)
        minpos[labels[::-1]] = positions[::-1]
        result += [minpos[idxs]]
    if find_max:
        maxs = np.zeros(labels.max() + 2, input.dtype)
        maxs[labels] = input
        result += [maxs[idxs]]
    if find_max_positions:
        maxpos = np.zeros(labels.max() + 2, int)
        maxpos[labels] = positions
        result += [maxpos[idxs]]
    if find_median:
        locs = np.arange(len(labels))
        lo = np.zeros(labels.max() + 2, np.int_)
        lo[labels[::-1]] = locs[::-1]
        hi = np.zeros(labels.max() + 2, np.int_)
        hi[labels] = locs
        lo = lo[idxs]
        hi = hi[idxs]
        # lo is an index to the lowest value in input for each label,
        # hi is an index to the largest value.
        # move them to be either the same ((hi - lo) % 2 == 0) or next
        # to each other ((hi - lo) % 2 == 1), then average.
        step = (hi - lo) // 2
        lo += step
        hi -= step
        if (np.issubdtype(input.dtype, np.integer)
                or np.issubdtype(input.dtype, np.bool_)):
            # avoid integer overflow or boolean addition (gh-12836)
            result += [(input[lo].astype('d') + input[hi].astype('d')) / 2.0]
        else:
            result += [(input[lo] + input[hi]) / 2.0]

    return result

