
def test_subset_chained_getitem_column(backend, dtype):
    # Case: creating a subset using multiple, chained getitem calls using views
    # still needs to guarantee proper CoW behaviour
    dtype_backend, DataFrame, Series = backend
    df = DataFrame(
        {"a": [1, 2, 3], "b": [4, 5, 6], "c": np.array([7, 8, 9], dtype=dtype)}
    )
    df_orig = df.copy()

    # modify subset -> don't modify parent
    subset = df[:]["a"][0:2]
    subset.iloc[0] = 0
    tm.assert_frame_equal(df, df_orig)

    # modify parent -> don't modify subset
    subset = df[:]["a"][0:2]
    df.iloc[0, 0] = 0
    expected = Series([1, 2], name="a")
    tm.assert_series_equal(subset, expected)

