
def test_read_hdf_index_not_view(temp_h5_path):
    # GH 37441
    # Ensure that the index of the DataFrame is not a view
    # into the original recarray that pytables reads in
    df = DataFrame(
        np.random.default_rng(2).random((4, 5)),
        index=[0, 1, 2, 3],
        columns=list("ABCDE"),
    )

    df.to_hdf(temp_h5_path, key="df", mode="w", format="table")

    df2 = read_hdf(temp_h5_path, "df")
    assert df2.index._data.base is None
    tm.assert_frame_equal(df, df2)

