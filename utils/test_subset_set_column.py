
def test_subset_set_column(backend):
    # Case: setting a single column on a viewing subset -> subset[col] = value
    dtype_backend, DataFrame, _ = backend
    df = DataFrame({"a": [1, 2, 3], "b": [4, 5, 6], "c": [0.1, 0.2, 0.3]})
    df_orig = df.copy()
    subset = df[1:3]

    if dtype_backend == "numpy":
        arr = np.array([10, 11], dtype="int64")
    else:
        arr = pd.array([10, 11], dtype="Int64")

    subset["a"] = arr
    subset._mgr._verify_integrity()
    expected = DataFrame(
        {"a": [10, 11], "b": [5, 6], "c": [0.2, 0.3]}, index=range(1, 3)
    )
    tm.assert_frame_equal(subset, expected)
    tm.assert_frame_equal(df, df_orig)

