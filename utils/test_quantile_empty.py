
def test_quantile_empty(dtype):
    # we should get back np.nans, not -1s
    arr = NumpyExtensionArray(np.array([], dtype=dtype))
    idx = pd.Index([0.0, 0.5])

    result = arr._quantile(idx, interpolation="linear")
    expected = NumpyExtensionArray(np.array([np.nan, np.nan]))
    tm.assert_extension_array_equal(result, expected)

