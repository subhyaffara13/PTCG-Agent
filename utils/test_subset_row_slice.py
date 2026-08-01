
def test_subset_row_slice(backend):
    # Case: taking a subset of the rows of a DataFrame using a slice
    # + afterwards modifying the subset
    _, DataFrame, _ = backend
    df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [0.1, 0.2, 0.3]})
    df_orig = df.copy()

    subset = df[1:3]
    subset._mgr._verify_integrity()

    assert subset.columns is not df.columns
    assert np.shares_memory(get_array(subset, "a"), get_array(df, "a"))

    subset.iloc[0, 0] = 0
    assert not np.shares_memory(get_array(subset, "a"), get_array(df, "a"))

    subset._mgr._verify_integrity()

    expected = DataFrame({"a": [0, 3], "b": [5, 6], "c": [0.2, 0.3]}, index=range(1, 3))
    tm.assert_frame_equal(subset, expected)
    # original parent dataframe is not modified (CoW)
    tm.assert_frame_equal(df, df_orig)

