
def test_categorical_nan_only_columns(temp_h5_path):
    # GH18413
    # Check that read_hdf with categorical columns with NaN-only values can
    # be read back.
    df = DataFrame(
        {
            "a": ["a", "b", "c", np.nan],
            "b": [np.nan, np.nan, np.nan, np.nan],
            "c": [1, 2, 3, 4],
            "d": Series([None] * 4, dtype=object),
        }
    )
    df["a"] = df.a.astype("category")
    df["b"] = df.b.astype("category")
    df["d"] = df.b.astype("category")
    expected = df
    df.to_hdf(temp_h5_path, key="df", format="table", data_columns=True)
    result = read_hdf(temp_h5_path, "df")
    tm.assert_frame_equal(result, expected)

