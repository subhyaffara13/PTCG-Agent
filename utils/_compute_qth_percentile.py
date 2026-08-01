
def _compute_qth_percentile(sorted_, per, interpolation_method, axis):
    if not np.isscalar(per):
        score = [_compute_qth_percentile(sorted_, i,
                                         interpolation_method, axis)
                 for i in per]
        return np.array(score)

    if not (0 <= per <= 100):
        raise ValueError("percentile must be in the range [0, 100]")

    indexer = [slice(None)] * sorted_.ndim
    idx = per / 100. * (sorted_.shape[axis] - 1)

    if int(idx) != idx:
        # round fractional indices according to interpolation method
        if interpolation_method == 'lower':
            idx = int(np.floor(idx))
        elif interpolation_method == 'higher':
            idx = int(np.ceil(idx))
        elif interpolation_method == 'fraction':
            pass  # keep idx as fraction and interpolate
        else:
            raise ValueError("interpolation_method can only be 'fraction', "
                             "'lower' or 'higher'")

    i = int(idx)
    if i == idx:
        indexer[axis] = slice(i, i + 1)
        weights = array(1)
        sumval = 1.0
    else:
        indexer[axis] = slice(i, i + 2)
        j = i + 1
        weights = array([(j - idx), (idx - i)], float)
        wshape = [1] * sorted_.ndim
        wshape[axis] = 2
        weights = weights.reshape(wshape)
        sumval = weights.sum()

    # Use np.add.reduce (== np.sum but a little faster) to coerce data type
    return np.add.reduce(sorted_[tuple(indexer)] * weights, axis=axis) / sumval

