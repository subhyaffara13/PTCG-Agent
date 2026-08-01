
def take_2d_multi(
    arr: np.ndarray,
    indexer: tuple[npt.NDArray[np.intp], npt.NDArray[np.intp]],
    fill_value=np.nan,
) -> np.ndarray:
    """
    Specialized Cython take which sets NaN values in one pass.
    """
    # This is only called from one place in DataFrame._reindex_multi,
    #  so we know indexer is well-behaved.
    assert indexer is not None
    assert indexer[0] is not None
    assert indexer[1] is not None

    row_idx, col_idx = indexer

    row_idx = ensure_platform_int(row_idx)
    col_idx = ensure_platform_int(col_idx)
    indexer = row_idx, col_idx
    mask_info = None

    # check for promotion based on types only (do this first because
    # it's faster than computing a mask)
    dtype, fill_value = maybe_promote(arr.dtype, fill_value)
    if dtype != arr.dtype:
        # check if promotion is actually required based on indexer
        row_mask = row_idx == -1
        col_mask = col_idx == -1
        row_needs = row_mask.any()
        col_needs = col_mask.any()
        mask_info = (row_mask, col_mask), (row_needs, col_needs)

        if not (row_needs or col_needs):
            # if not, then depromote, set fill_value to dummy
            # (it won't be used but we don't want the cython code
            # to crash when trying to cast it to dtype)
            dtype, fill_value = arr.dtype, arr.dtype.type()

    # at this point, it's guaranteed that dtype can hold both the arr values
    # and the fill_value
    out_shape = len(row_idx), len(col_idx)
    out = np.empty(out_shape, dtype=dtype)

    func = _take_2d_multi_dict.get((arr.dtype.name, out.dtype.name), None)
    if func is None and arr.dtype != out.dtype:
        func = _take_2d_multi_dict.get((out.dtype.name, out.dtype.name), None)
        if func is not None:
            func = _convert_wrapper(func, out.dtype)

    if func is not None:
        func(arr, indexer, out=out, fill_value=fill_value)
    else:
        # test_reindex_multi
        _take_2d_multi_object(
            arr, indexer, out, fill_value=fill_value, mask_info=mask_info
        )

    return out

