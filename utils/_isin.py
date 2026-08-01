
def _isin(ar1, ar2, assume_unique=False, invert=False, *, kind=None):
    # Ravel both arrays, behavior for the first array could be different
    ar1 = np.asarray(ar1).ravel()
    ar2 = np.asarray(ar2).ravel()

    # Ensure that iteration through object arrays yields size-1 arrays
    if ar2.dtype == object:
        ar2 = ar2.reshape(-1, 1)

    if kind not in {None, 'sort', 'table'}:
        raise ValueError(
            f"Invalid kind: '{kind}'. Please use None, 'sort' or 'table'.")

    # Can use the table method if all arrays are integers or boolean:
    is_int_arrays = all(ar.dtype.kind in ("u", "i", "b") for ar in (ar1, ar2))
    use_table_method = is_int_arrays and kind in {None, 'table'}

    if use_table_method:
        if ar2.size == 0:
            if invert:
                return np.ones_like(ar1, dtype=bool)
            else:
                return np.zeros_like(ar1, dtype=bool)

        # Convert booleans to uint8 so we can use the fast integer algorithm
        if ar1.dtype == bool:
            ar1 = ar1.astype(np.uint8)
        if ar2.dtype == bool:
            ar2 = ar2.astype(np.uint8)

        ar2_min = int(np.min(ar2))
        ar2_max = int(np.max(ar2))

        ar2_range = ar2_max - ar2_min

        # Constraints on whether we can actually use the table method:
        #  1. Assert memory usage is not too large
        below_memory_constraint = ar2_range <= 6 * (ar1.size + ar2.size)
        #  2. Check overflows for (ar2 - ar2_min); dtype=ar2.dtype
        range_safe_from_overflow = ar2_range <= np.iinfo(ar2.dtype).max

        # Optimal performance is for approximately
        # log10(size) > (log10(range) - 2.27) / 0.927.
        # However, here we set the requirement that by default
        # the intermediate array can only be 6x
        # the combined memory allocation of the original
        # arrays. See discussion on
        # https://github.com/numpy/numpy/pull/12065.

        if (
            range_safe_from_overflow and
            (below_memory_constraint or kind == 'table')
        ):

            if invert:
                outgoing_array = np.ones_like(ar1, dtype=bool)
            else:
                outgoing_array = np.zeros_like(ar1, dtype=bool)

            # Make elements 1 where the integer exists in ar2
            if invert:
                isin_helper_ar = np.ones(ar2_range + 1, dtype=bool)
                isin_helper_ar[ar2 - ar2_min] = 0
            else:
                isin_helper_ar = np.zeros(ar2_range + 1, dtype=bool)
                isin_helper_ar[ar2 - ar2_min] = 1

            # Mask out elements we know won't work
            basic_mask = (ar1 <= ar2_max) & (ar1 >= ar2_min)
            in_range_ar1 = ar1[basic_mask]
            if in_range_ar1.size == 0:
                # Nothing more to do, since all values are out of range.
                return outgoing_array

            # Unfortunately, ar2_min can be out of range for `intp` even
            # if the calculation result must fit in range (and be positive).
            # In that case, use ar2.dtype which must work for all unmasked
            # values.
            try:
                ar2_min = np.array(ar2_min, dtype=np.intp)
                dtype = np.intp
            except OverflowError:
                dtype = ar2.dtype

            out = np.empty_like(in_range_ar1, dtype=np.intp)
            outgoing_array[basic_mask] = isin_helper_ar[
                    np.subtract(in_range_ar1, ar2_min, dtype=dtype,
                                out=out, casting="unsafe")]

            return outgoing_array
        elif kind == 'table':  # not range_safe_from_overflow
            raise RuntimeError(
                "You have specified kind='table', "
                "but the range of values in `ar2` or `ar1` exceed the "
                "maximum integer of the datatype. "
                "Please set `kind` to None or 'sort'."
            )
    elif kind == 'table':
        raise ValueError(
            "The 'table' method is only "
            "supported for boolean or integer arrays. "
            "Please select 'sort' or None for kind."
        )

    # Check if one of the arrays may contain arbitrary objects
    contains_object = ar1.dtype.hasobject or ar2.dtype.hasobject

    # This code is run when
    # a) the first condition is true, making the code significantly faster
    # b) the second condition is true (i.e. `ar1` or `ar2` may contain
    #    arbitrary objects), since then sorting is not guaranteed to work
    if len(ar2) < 10 * len(ar1) ** 0.145 or contains_object:
        if invert:
            mask = np.ones(len(ar1), dtype=bool)
            for a in ar2:
                mask &= (ar1 != a)
        else:
            mask = np.zeros(len(ar1), dtype=bool)
            for a in ar2:
                mask |= (ar1 == a)
        return mask

    # Otherwise use sorting
    if not assume_unique:
        ar1, rev_idx = np.unique(ar1, return_inverse=True)
        ar2 = np.unique(ar2)

    ar = np.concatenate((ar1, ar2))
    # We need this to be a stable sort, so always use 'mergesort'
    # here. The values from the first array should always come before
    # the values from the second array.
    order = ar.argsort(kind='mergesort')
    sar = ar[order]
    if invert:
        bool_ar = (sar[1:] != sar[:-1])
    else:
        bool_ar = (sar[1:] == sar[:-1])
    flag = np.concatenate((bool_ar, [invert]))
    ret = np.empty(ar.shape, dtype=bool)
    ret[order] = flag

    if assume_unique:
        return ret[:len(ar1)]
    else:
        return ret[rev_idx]

