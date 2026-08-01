
def test_pickle_path_pathlib(temp_file):
    df = DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=Index(list("ABCD"), dtype=object),
        index=Index([f"i-{i}" for i in range(30)], dtype=object),
    )
    result = tm.round_trip_pathlib(df.to_pickle, pd.read_pickle, temp_file)
    tm.assert_frame_equal(df, result)

