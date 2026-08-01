
def test_subset_column_selection(backend):
    # Case: taking a subset of the columns of a DataFrame
    # + afterwards modifying the subset
    _, DataFrame, _ = backend
    df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [0.1, 0.2, 0.3]})
    df_orig = df.copy()

    subset = df[["a", "c"]]

    assert subset.index is not df.index

    # the subset shares memory ...
    assert np.shares_memory(get_array(subset, "a"), get_array(df, "a"))
    # ... but uses CoW when being modified
    subset.iloc[0, 0] = 0

    assert not np.shares_memory(get_array(subset, "a"), get_array(df, "a"))

    expected = DataFrame({"a": [0, 2, 3], "c": [0.1, 0.2, 0.3]})
    tm.assert_frame_equal(subset, expected)
    tm.assert_frame_equal(df, df_orig)

