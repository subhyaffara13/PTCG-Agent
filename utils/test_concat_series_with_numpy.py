
def test_concat_series_with_numpy(to_concat_dtypes, result_dtype):
    # we expect the same dtypes as we would get with non-masked inputs,
    #  just masked where available.

    s1 = pd.Series([0, 1, pd.NA], dtype=to_concat_dtypes[0])
    s2 = pd.Series(np.array([0, 1], dtype=to_concat_dtypes[1]))
    result = pd.concat([s1, s2], ignore_index=True)
    expected = pd.Series([0, 1, pd.NA, 0, 1], dtype=object).astype(result_dtype)
    tm.assert_series_equal(result, expected)

    # order doesn't matter for result
    result = pd.concat([s2, s1], ignore_index=True)
    expected = pd.Series([0, 1, 0, 1, pd.NA], dtype=object).astype(result_dtype)
    tm.assert_series_equal(result, expected)

