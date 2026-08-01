
def test_series_constructor_with_astype():
    ndarray = np.array([1, 2, 3])
    result = pd.Series(NumpyExtensionArray(ndarray), dtype="float64")
    expected = pd.Series([1.0, 2.0, 3.0], dtype="float64")
    tm.assert_series_equal(result, expected)

