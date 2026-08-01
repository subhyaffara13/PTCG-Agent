
def test_read_nokey(temp_h5_path):
    # GH10443
    df = DataFrame(
        np.random.default_rng(2).random((4, 5)),
        index=list("abcd"),
        columns=list("ABCDE"),
    )

    # Categorical dtype not supported for "fixed" format. So no need
    # to test with that dtype in the dataframe here.
    df.to_hdf(temp_h5_path, key="df", mode="a")
    reread = read_hdf(temp_h5_path)
    tm.assert_frame_equal(df, reread)
    df.to_hdf(temp_h5_path, key="df2", mode="a")

    msg = "key must be provided when HDF5 file contains multiple datasets."
    with pytest.raises(ValueError, match=msg):
        read_hdf(temp_h5_path)

