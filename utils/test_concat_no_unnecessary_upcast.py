
def test_concat_no_unnecessary_upcast(float_numpy_dtype, frame_or_series):
    # GH 13247
    dims = frame_or_series(dtype=object).ndim
    dt = float_numpy_dtype

    dfs = [
        frame_or_series(np.array([1], dtype=dt, ndmin=dims)),
        frame_or_series(np.array([np.nan], dtype=dt, ndmin=dims)),
        frame_or_series(np.array([5], dtype=dt, ndmin=dims)),
    ]
    x = concat(dfs)
    assert x.values.dtype == dt

