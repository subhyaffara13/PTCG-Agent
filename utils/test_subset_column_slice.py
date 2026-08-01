
def test_subset_column_slice(backend, dtype):
    # Case: taking a subset of the columns of a DataFrame using a slice
    # + afterwards modifying the subset
    dtype_backend, DataFrame, _ = backend
    df = DataFrame(
        {"a": [1, 2, 3], "b": [4, 5, 6], "c": np.array([7, 8, 9], dtype=dtype)}
    )
    df_orig = df.copy()

    subset = df.iloc[:, 1:]
    subset._mgr._verify_integrity()

    assert subset.index is not df.index
    assert np.shares_memory(get_array(subset, "b"), get_array(df, "b"))

    subset.iloc[0, 0] = 0
    assert not np.shares_memory(get_array(subset, "b"), get_array(df, "b"))

    expected = DataFrame({"b": [0, 5, 6], "c": np.array([7, 8, 9], dtype=dtype)})
    tm.assert_frame_equal(subset, expected)
    # original parent dataframe is not modified (also not for BlockManager case,
    # except for single block)
    tm.assert_frame_equal(df, df_orig)

