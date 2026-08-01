
def test_subset_set_with_column_indexer(backend, indexer):
    # Case: setting multiple columns with a column indexer on a viewing subset
    # -> subset.loc[:, [col1, col2]] = value
    _, DataFrame, _ = backend
    df = DataFrame({"a": [1, 2, 3], "b": [0.1, 0.2, 0.3], "c": [4, 5, 6]})
    df_orig = df.copy()
    subset = df[1:3]

    subset.loc[:, indexer] = 0

    subset._mgr._verify_integrity()
    expected = DataFrame({"a": [0, 0], "b": [0.0, 0.0], "c": [5, 6]}, index=range(1, 3))
    tm.assert_frame_equal(subset, expected)
    tm.assert_frame_equal(df, df_orig)

