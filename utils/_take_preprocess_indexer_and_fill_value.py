
def _take_preprocess_indexer_and_fill_value(
    arr: np.ndarray,
    indexer: npt.NDArray[np.intp],
    fill_value,
    allow_fill: bool,
    mask: npt.NDArray[np.bool_] | None = None,
):
    mask_info: tuple[np.ndarray | None, bool] | None = None

    if not allow_fill:
        dtype, fill_value = arr.dtype, arr.dtype.type()
        mask_info = None, False
    else:
        # check for promotion based on types only (do this first because
        # it's faster than computing a mask)
        dtype, fill_value = maybe_promote(arr.dtype, fill_value)
        if dtype != arr.dtype:
            # check if promotion is actually required based on indexer
            if mask is not None:
                needs_masking = True
            else:
                mask = indexer == -1
                needs_masking = bool(mask.any())
            mask_info = mask, needs_masking
            if not needs_masking:
                # if not, then depromote, set fill_value to dummy
                # (it won't be used but we don't want the cython code
                # to crash when trying to cast it to dtype)
                dtype, fill_value = arr.dtype, arr.dtype.type()

    return dtype, fill_value, mask_info

