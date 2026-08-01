
def test_to_numpy_float():
    # GH#56267
    ser = pd.Series([32, 40, None], dtype="float[pyarrow]")
    result = ser.astype("float64")
    expected = pd.Series([32, 40, np.nan], dtype="float64")
    tm.assert_series_equal(result, expected)


def test_to_numpy_float(box):
    con = pd.Series if box else pd.array

    # no missing values -> can convert to float, otherwise raises
    arr = con([0.1, 0.2, 0.3], dtype="Float64")
    result = arr.to_numpy(dtype="float64")
    expected = np.array([0.1, 0.2, 0.3], dtype="float64")
    tm.assert_numpy_array_equal(result, expected)

    arr = con([0.1, 0.2, None], dtype="Float64")
    result = arr.to_numpy(dtype="float64")
    expected = np.array([0.1, 0.2, np.nan], dtype="float64")
    tm.assert_numpy_array_equal(result, expected)

    result = arr.to_numpy(dtype="float64", na_value=np.nan)
    expected = np.array([0.1, 0.2, np.nan], dtype="float64")
    tm.assert_numpy_array_equal(result, expected)

