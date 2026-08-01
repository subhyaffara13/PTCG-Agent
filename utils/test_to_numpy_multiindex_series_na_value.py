
def test_to_numpy_multiindex_series_na_value(
    data, multiindex, dtype, na_value, expected
):
    index = pd.MultiIndex.from_tuples(multiindex)
    series = Series(data, index=index)
    result = series.to_numpy(dtype=dtype, na_value=na_value)
    expected = np.array(expected)
    tm.assert_numpy_array_equal(result, expected)

