
def _median(lst):
    assert len(lst) > 0
    return torch.median(torch.tensor(lst)).item()


def _median(a, axis=None, out=None, overwrite_input=False):
    # can't be reasonably be implemented in terms of percentile as we have to
    # call mean to not break astropy
    a = np.asanyarray(a)

    # Set the partition indexes
    if axis is None:
        sz = a.size
    else:
        sz = a.shape[axis]
    if sz % 2 == 0:
        szh = sz // 2
        kth = [szh - 1, szh]
    else:
        kth = [(sz - 1) // 2]

    # We have to check for NaNs (as of writing 'M' doesn't actually work).
    supports_nans = np.issubdtype(a.dtype, np.inexact) or a.dtype.kind in 'Mm'
    if supports_nans:
        kth.append(-1)

    if overwrite_input:
        if axis is None:
            part = a.ravel()
            part.partition(kth)
        else:
            a.partition(kth, axis=axis)
            part = a
    else:
        part = partition(a, kth, axis=axis)

    if part.shape == ():
        # make 0-D arrays work
        return part.item()
    if axis is None:
        axis = 0

    indexer = [slice(None)] * part.ndim
    index = part.shape[axis] // 2
    if part.shape[axis] % 2 == 1:
        # index with slice to allow mean (below) to work
        indexer[axis] = slice(index, index + 1)
    else:
        indexer[axis] = slice(index - 1, index + 1)
    indexer = tuple(indexer)

    # Use mean in both odd and even case to coerce data type,
    # using out array if needed.
    rout = mean(part[indexer], axis=axis, out=out)
    if supports_nans and sz > 0:
        # If nans are possible, warn and replace by nans like mean would.
        rout = np.lib._utils_impl._median_nancheck(part, rout, axis)

    return rout


def _median(a, axis=None, out=None, overwrite_input=False):
    # when an unmasked NaN is present return it, so we need to sort the NaN
    # values behind the mask
    if np.issubdtype(a.dtype, np.inexact):
        fill_value = np.inf
    else:
        fill_value = None
    if overwrite_input:
        if axis is None:
            asorted = a.ravel()
            asorted.sort(fill_value=fill_value)
        else:
            a.sort(axis=axis, fill_value=fill_value)
            asorted = a
    else:
        asorted = sort(a, axis=axis, fill_value=fill_value)

    if axis is None:
        axis = 0
    else:
        axis = normalize_axis_index(axis, asorted.ndim)

    if asorted.shape[axis] == 0:
        # for empty axis integer indices fail so use slicing to get same result
        # as median (which is mean of empty slice = nan)
        indexer = [slice(None)] * asorted.ndim
        indexer[axis] = slice(0, 0)
        indexer = tuple(indexer)
        return np.ma.mean(asorted[indexer], axis=axis, out=out)

    if asorted.ndim == 1:
        idx, odd = divmod(count(asorted), 2)
        mid = asorted[idx + odd - 1:idx + 1]
        if np.issubdtype(asorted.dtype, np.inexact) and asorted.size > 0:
            # avoid inf / x = masked
            s = mid.sum(out=out)
            if not odd:
                s = np.true_divide(s, 2., casting='safe', out=out)
            s = np.lib._utils_impl._median_nancheck(asorted, s, axis)
        else:
            s = mid.mean(out=out)

        # if result is masked either the input contained enough
        # minimum_fill_value so that it would be the median or all values
        # masked
        if np.ma.is_masked(s) and not np.all(asorted.mask):
            return np.ma.minimum_fill_value(asorted)
        return s

    counts = count(asorted, axis=axis, keepdims=True)
    h = counts // 2

    # duplicate high if odd number of elements so mean does nothing
    odd = counts % 2 == 1
    l = np.where(odd, h, h - 1)

    lh = np.concatenate([l, h], axis=axis)

    # get low and high median
    low_high = np.take_along_axis(asorted, lh, axis=axis)

    def replace_masked(s):
        # Replace masked entries with minimum_full_value unless it all values
        # are masked. This is required as the sort order of values equal or
        # larger than the fill value is undefined and a valid value placed
        # elsewhere, e.g. [4, --, inf].
        if np.ma.is_masked(s):
            rep = (~np.all(asorted.mask, axis=axis, keepdims=True)) & s.mask
            s.data[rep] = np.ma.minimum_fill_value(asorted)
            s.mask[rep] = False

    replace_masked(low_high)

    if np.issubdtype(asorted.dtype, np.inexact):
        # avoid inf / x = masked
        s = np.ma.sum(low_high, axis=axis, out=out)
        np.true_divide(s.data, 2., casting='unsafe', out=s.data)

        s = np.lib._utils_impl._median_nancheck(asorted, s, axis)
    else:
        s = np.ma.mean(low_high, axis=axis, out=out)

    return s

