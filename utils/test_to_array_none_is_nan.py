
def test_to_array_none_is_nan(a, b, using_nan_is_na):
    result = pd.array(a, dtype="Float64")
    expected = pd.array(b, dtype="Float64")
    if not using_nan_is_na and a[-1] is np.nan:
        assert np.isnan(result[-1])
        expected._mask[-1] = False
    tm.assert_extension_array_equal(result, expected)

