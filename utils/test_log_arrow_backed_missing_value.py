
def test_log_arrow_backed_missing_value(using_nan_is_na):
    # GH#56285
    ser = Series([1, 2, None], dtype="float64[pyarrow]")
    if using_nan_is_na:
        result = np.log(ser)
        expected = np.log(Series([1, 2, None], dtype="float64[pyarrow]"))
        tm.assert_series_equal(result, expected)
    else:
        # we get cast to object which raises
        msg = "loop of ufunc does not support argument"
        with pytest.raises(TypeError, match=msg):
            np.log(ser)

