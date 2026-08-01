
def test_subset_chained_getitem(
    request,
    backend,
    method,
    dtype,
):
    # Case: creating a subset using multiple, chained getitem calls using views
    # still needs to guarantee proper CoW behaviour
    _, DataFrame, _ = backend
    df = DataFrame(
        {"a": [1, 2, 3], "b": [4, 5, 6], "c": np.array([7, 8, 9], dtype=dtype)}
    )
    df_orig = df.copy()

    # modify subset -> don't modify parent
    subset = method(df)

    subset.iloc[0, 0] = 0
    tm.assert_frame_equal(df, df_orig)

    # modify parent -> don't modify subset
    subset = method(df)
    df.iloc[0, 0] = 0
    expected = DataFrame({"a": [1, 2], "b": [4, 5]})
    tm.assert_frame_equal(subset, expected)

