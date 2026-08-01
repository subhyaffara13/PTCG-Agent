
def test_ufunc_retains_missing():
    # GH#62800
    ser = pd.Series([0.1, pd.NA], dtype="float64[pyarrow]")

    result = np.sin(ser)

    expected = pd.Series([np.sin(0.1), pd.NA], dtype="float64[pyarrow]")
    tm.assert_series_equal(result, expected)

