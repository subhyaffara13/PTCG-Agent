
def _get_next_label(label):
    # see test_slice_locs_with_ints_and_floats_succeeds
    dtype = getattr(label, "dtype", type(label))
    if isinstance(label, (Timestamp, Timedelta)):
        dtype = "datetime64[ns]"
    dtype = pandas_dtype(dtype)

    if lib.is_np_dtype(dtype, "mM") or isinstance(dtype, DatetimeTZDtype):
        return label + np.timedelta64(1, "ns")
    elif is_integer_dtype(dtype):
        return label + 1
    elif is_float_dtype(dtype):
        return np.nextafter(label, np.inf)
    else:
        raise TypeError(f"cannot determine next label for type {type(label)!r}")

