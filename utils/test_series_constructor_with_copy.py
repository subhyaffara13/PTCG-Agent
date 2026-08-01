
def test_series_constructor_with_copy():
    ndarray = np.array([1, 2, 3])
    ser = pd.Series(NumpyExtensionArray(ndarray), copy=True)

    assert ser.values is not ndarray

