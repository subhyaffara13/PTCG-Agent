
def test_subset_set_column_with_loc2(backend):
    # Case: setting a single column with loc on a viewing subset
    # -> subset.loc[:, col] = value
    # separate test for case of DataFrame of a single column -> takes a separate
    # code path
    _, DataFrame, _ = backend
    df = DataFrame({"a": [1, 2, 3]})
    df_orig = df.copy()
    subset = df[1:3]

    subset.loc[:, "a"] = 0

    subset._mgr._verify_integrity()
    expected = DataFrame({"a": [0, 0]}, index=range(1, 3))
    tm.assert_frame_equal(subset, expected)
    # original parent dataframe is not modified (CoW)
    tm.assert_frame_equal(df, df_orig)

