
def _safe_fill_null(
    arr: pa.Array | pa.ChunkedArray, fill_value: Any
) -> pa.Array | pa.ChunkedArray:
    """
    Safe wrapper for pyarrow.compute.fill_null with fallback for Windows + pyarrow 21.

    pyarrow 21.0.0 on Windows has a bug in fill_null that incorrectly fills null values.
    This function uses a fallback implementation for that specific case, otherwise uses
    the standard pyarrow.compute.fill_null.

    Parameters
    ----------
    arr : pyarrow.Array | pyarrow.ChunkedArray
        Input array with potential null values.
    fill_value : Any
        Value to fill nulls with.

    Returns
    -------
    pyarrow.Array | pyarrow.ChunkedArray
        Array with nulls filled with fill_value.
    """
    import pyarrow.compute as pc

    is_windows = sys.platform in ["win32", "cygwin"]
    use_fallback = (
        HAS_PYARROW and is_windows and not pa_version_under21p0 and pa_version_under22p0
    )
    if not use_fallback or isinstance(fill_value, (pa.Array, pa.ChunkedArray)):
        return pc.fill_null(arr, fill_value)

    fill_scalar = pa.scalar(fill_value, type=arr.type)

    if pa.types.is_duration(arr.type):

        def fill_null_duration(arr: pa.Array, fill_scalar: pa.Scalar) -> pa.Array:
            mask = pc.is_null(arr)
            zero_duration = pa.scalar(0, type=arr.type)
            arr_zeroed = pc.if_else(mask, zero_duration, arr)
            return pc.if_else(mask, fill_scalar, arr_zeroed)

        if isinstance(arr, pa.ChunkedArray):
            return pa.chunked_array(
                [fill_null_duration(chunk, fill_scalar) for chunk in arr.chunks]
            )
        return fill_null_duration(arr, fill_scalar)

    if isinstance(arr, pa.ChunkedArray):
        return pa.chunked_array(
            [pc.if_else(pc.is_null(chunk), fill_scalar, chunk) for chunk in arr.chunks]
        )
    return pc.if_else(pc.is_null(arr), fill_scalar, arr)

