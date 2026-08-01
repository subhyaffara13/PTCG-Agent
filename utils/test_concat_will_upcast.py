
def test_concat_will_upcast(frame_or_series, any_signed_int_numpy_dtype):
    dt = any_signed_int_numpy_dtype
    dims = frame_or_series().ndim
    dfs = [
        frame_or_series(np.array([1], dtype=dt, ndmin=dims)),
        frame_or_series(np.array([np.nan], ndmin=dims)),
        frame_or_series(np.array([5], dtype=dt, ndmin=dims)),
    ]
    x = concat(dfs)
    assert x.values.dtype == "float64"

