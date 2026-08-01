
def test_api_append(temp_h5_path):
    path = temp_h5_path

    df = DataFrame(range(20))
    df.iloc[:10].to_hdf(path, key="df", append=True)
    df.iloc[10:].to_hdf(path, key="df", append=True, format="table")
    tm.assert_frame_equal(read_hdf(path, "df"), df)

    # append to False
    df.iloc[:10].to_hdf(path, key="df", append=False, format="table")
    df.iloc[10:].to_hdf(path, key="df", append=True)
    tm.assert_frame_equal(read_hdf(path, "df"), df)

