
def test_read_nokey_table(temp_h5_path):
    # GH13231
    df = DataFrame({"i": range(5), "c": Series(list("abacd"), dtype="category")})

    df.to_hdf(temp_h5_path, key="df", mode="a", format="table")
    reread = read_hdf(temp_h5_path)
    tm.assert_frame_equal(df, reread)
    df.to_hdf(temp_h5_path, key="df2", mode="a", format="table")

    msg = "key must be provided when HDF5 file contains multiple datasets."
    with pytest.raises(ValueError, match=msg):
        read_hdf(temp_h5_path)

