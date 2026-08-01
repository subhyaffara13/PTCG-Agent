
def test_subset_set_columns(backend, dtype):
    # Case: setting multiple columns on a viewing subset
    # -> subset[[col1, col2]] = value
    dtype_backend, DataFrame, _ = backend
    df = DataFrame(
        {"a": [1, 2, 3], "b": [4, 5, 6], "c": np.array([7, 8, 9], dtype=dtype)}
    )
    df_orig = df.copy()
    subset = df[1:3]

    subset[["a", "c"]] = 0

    subset._mgr._verify_integrity()
    # first and third column should certainly have no references anymore
    assert all(subset._mgr._has_no_reference(i) for i in [0, 2])
    expected = DataFrame({"a": [0, 0], "b": [5, 6], "c": [0, 0]}, index=range(1, 3))
    if dtype_backend == "nullable":
        # there is not yet a global option, so overriding a column by setting a scalar
        # defaults to numpy dtype even if original column was nullable
        expected["a"] = expected["a"].astype("int64")
        expected["c"] = expected["c"].astype("int64")

    tm.assert_frame_equal(subset, expected)
    tm.assert_frame_equal(df, df_orig)

