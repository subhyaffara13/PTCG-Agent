
def test_idxmin_idxmax_extremes(how, any_real_numpy_dtype):
    # GH#57040
    if any_real_numpy_dtype is int or any_real_numpy_dtype is float:
        # No need to test
        return
    info = np.iinfo if "int" in any_real_numpy_dtype else np.finfo
    min_value = info(any_real_numpy_dtype).min
    max_value = info(any_real_numpy_dtype).max
    df = DataFrame(
        {"a": [2, 1, 1, 2], "b": [min_value, max_value, max_value, min_value]},
        dtype=any_real_numpy_dtype,
    )
    gb = df.groupby("a")
    result = getattr(gb, how)()
    expected = DataFrame(
        {"b": [1, 0]}, index=pd.Index([1, 2], name="a", dtype=any_real_numpy_dtype)
    )
    tm.assert_frame_equal(result, expected)

