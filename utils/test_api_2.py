
def test_api_2(temp_h5_path):
    df = DataFrame(range(20))
    df.to_hdf(temp_h5_path, key="df", append=False, format="fixed")
    tm.assert_frame_equal(read_hdf(temp_h5_path, "df"), df)

    df.to_hdf(temp_h5_path, key="df", append=False, format="f")
    tm.assert_frame_equal(read_hdf(temp_h5_path, "df"), df)

    df.to_hdf(temp_h5_path, key="df", append=False)
    tm.assert_frame_equal(read_hdf(temp_h5_path, "df"), df)

    df.to_hdf(temp_h5_path, key="df")
    tm.assert_frame_equal(read_hdf(temp_h5_path, "df"), df)

