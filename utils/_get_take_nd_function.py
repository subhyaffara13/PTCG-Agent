
def _get_take_nd_function(
    ndim: int,
    arr_dtype: np.dtype,
    out_dtype: np.dtype,
    axis: AxisInt = 0,
    mask_info=None,
):
    """
    Get the appropriate "take" implementation for the given dimension, axis
    and dtypes.
    """
    func = None
    if ndim <= 2:
        # for this part we don't need `mask_info` -> use the cached algo lookup
        func = _get_take_nd_function_cached(ndim, arr_dtype, out_dtype, axis)

    if func is None:

        def func(arr, indexer, out, fill_value=np.nan) -> None:
            indexer = ensure_platform_int(indexer)
            _take_nd_object(
                arr, indexer, out, axis=axis, fill_value=fill_value, mask_info=mask_info
            )

    return func

