
def _masked_arrays_2_sentinel_arrays(samples):
    # masked arrays in `samples` are converted to regular arrays, and values
    # corresponding with masked elements are replaced with a sentinel value

    # return without modifying arrays if none have a mask
    has_mask = False
    for sample in samples:
        mask = getattr(sample, 'mask', False)
        has_mask = has_mask or np.any(mask)
    if not has_mask:
        return samples, None  # None means there is no sentinel value

    # Choose a sentinel value. We can't use `np.nan`, because sentinel (masked)
    # values are always omitted, but there are different nan policies.
    dtype = np.result_type(*samples)
    dtype = dtype if np.issubdtype(dtype, np.number) else np.float64
    for i in range(len(samples)):
        # Things get more complicated if the arrays are of different types.
        # We could have different sentinel values for each array, but
        # the purpose of this code is convenience, not efficiency.
        samples[i] = samples[i].astype(dtype, copy=False)

    inexact = np.issubdtype(dtype, np.inexact)
    info = np.finfo if inexact else np.iinfo
    max_possible, min_possible = info(dtype).max, info(dtype).min
    nextafter = np.nextafter if inexact else (lambda x, _: x - 1)

    sentinel = max_possible
    # For simplicity, min_possible/np.infs are not candidate sentinel values
    while sentinel > min_possible:
        for sample in samples:
            if np.any(sample == sentinel):  # choose a new sentinel value
                sentinel = nextafter(sentinel, -np.inf)
                break
        else:  # when sentinel value is OK, break the while loop
            break
    else:
        message = ("This function replaces masked elements with sentinel "
                   "values, but the data contains all distinct values of this "
                   "data type. Consider promoting the dtype to `np.float64`.")
        raise ValueError(message)

    # replace masked elements with sentinel value
    out_samples = []
    for sample in samples:
        mask = getattr(sample, 'mask', None)
        if mask is not None:  # turn all masked arrays into sentinel arrays
            mask = np.broadcast_to(mask, sample.shape)
            sample = sample.data.copy() if np.any(mask) else sample.data
            sample = np.asarray(sample)  # `sample.data` could be a memoryview?
            sample[mask] = sentinel
        out_samples.append(sample)

    return out_samples, sentinel

