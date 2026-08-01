
def nan_policy_1d(hypotest, data1d, unpacker, *args, n_outputs=2,
                  nan_policy='raise', paired=False, _no_deco=True, **kwds):
    # Reference implementation for how `nan_policy` should work for 1d samples

    if nan_policy == 'raise':
        for sample in data1d:
            if np.any(np.isnan(sample)):
                raise ValueError("The input contains nan values")

    elif (nan_policy == 'propagate'
          and hypotest not in override_propagate_funcs):
        # For all hypothesis tests tested, returning nans is the right thing.
        # But many hypothesis tests don't propagate correctly (e.g. they treat
        # np.nan the same as np.inf, which doesn't make sense when ranks are
        # involved) so override that behavior here.
        for sample in data1d:
            if np.any(np.isnan(sample)):
                return np.full(n_outputs, np.nan)

    elif nan_policy == 'omit':
        # manually omit nans (or pairs in which at least one element is nan)
        if not paired:
            data1d = [sample[~np.isnan(sample)] for sample in data1d]
        else:
            nan_mask = np.isnan(data1d[0])
            for sample in data1d[1:]:
                nan_mask = np.logical_or(nan_mask, np.isnan(sample))
            data1d = [sample[~nan_mask] for sample in data1d]

    return unpacker(hypotest(*data1d, *args, _no_deco=_no_deco, **kwds))

