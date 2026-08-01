
def test_path_pathlib_hdfstore(temp_h5_path):
    df = DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=Index(list("ABCD")),
        index=Index([f"i-{i}" for i in range(30)]),
    )

    def writer(path):
        with HDFStore(path) as store:
            df.to_hdf(store, key="df")

    def reader(path):
        with HDFStore(path) as store:
            return read_hdf(store, "df")

    result = tm.round_trip_pathlib(writer, reader, temp_h5_path)
    tm.assert_frame_equal(df, result)

