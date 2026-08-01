
def test_path_pathlib(temp_h5_path):
    df = DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=Index(list("ABCD")),
        index=Index([f"i-{i}" for i in range(30)]),
    )

    result = tm.round_trip_pathlib(
        lambda p: df.to_hdf(p, key="df"), lambda p: read_hdf(p, "df"), temp_h5_path
    )
    tm.assert_frame_equal(df, result)

