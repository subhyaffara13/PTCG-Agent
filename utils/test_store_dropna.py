
def test_store_dropna(temp_h5_path):
    df_with_missing = DataFrame(
        {"col1": [0.0, np.nan, 2.0], "col2": [1.0, np.nan, np.nan]},
        index=list("abc"),
    )
    df_without_missing = DataFrame(
        {"col1": [0.0, 2.0], "col2": [1.0, np.nan]}, index=list("ac")
    )

    # # Test to make sure defaults are to not drop.
    # # Corresponding to Issue 9382
    df_with_missing.to_hdf(temp_h5_path, key="df", format="table")
    reloaded = read_hdf(temp_h5_path, "df")
    tm.assert_frame_equal(df_with_missing, reloaded)

    df_with_missing.to_hdf(temp_h5_path, key="df", format="table", dropna=False)
    reloaded = read_hdf(temp_h5_path, "df")
    tm.assert_frame_equal(df_with_missing, reloaded)

    df_with_missing.to_hdf(temp_h5_path, key="df", format="table", dropna=True)
    reloaded = read_hdf(temp_h5_path, "df")
    tm.assert_frame_equal(df_without_missing, reloaded)

