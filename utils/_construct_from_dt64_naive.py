
def _construct_from_dt64_naive(
    data: np.ndarray, *, tz: tzinfo | None, copy: bool, ambiguous: TimeAmbiguous
) -> tuple[np.ndarray, bool]:
    """
    Convert datetime64 data to a supported dtype, localizing if necessary.
    """
    # Caller is responsible for ensuring
    #  lib.is_np_dtype(data.dtype)

    new_dtype = data.dtype
    if not is_supported_dtype(new_dtype):
        # Cast to the nearest supported unit, generally "s"
        new_dtype = get_supported_dtype(new_dtype)
        data = astype_overflowsafe(data, dtype=new_dtype, copy=False)
        copy = False

    if data.dtype.byteorder == ">":
        # TODO: better way to handle this?  non-copying alternative?
        #  without this, test_constructor_datetime64_bigendian fails
        data = data.astype(data.dtype.newbyteorder("<"))
        new_dtype = data.dtype
        copy = False

    if tz is not None:
        # Convert tz-naive to UTC
        # TODO: if tz is UTC, are there situations where we *don't* want a
        #  copy?  tz_localize_to_utc always makes one.
        shape = data.shape
        if data.ndim > 1:
            data = data.ravel()

        data_unit = get_unit_from_dtype(new_dtype)
        data = tzconversion.tz_localize_to_utc(
            data.view("i8"), tz, ambiguous=ambiguous, creso=data_unit
        )
        data = data.view(new_dtype)
        data = data.reshape(shape)

    assert data.dtype == new_dtype, data.dtype
    result = data

    return result, copy

