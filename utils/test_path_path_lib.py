
def test_path_path_lib(all_parsers, temp_file):
    parser = all_parsers
    df = DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=Index(list("ABCD")),
        index=Index([f"i-{i}" for i in range(30)]),
    )
    result = tm.round_trip_pathlib(
        df.to_csv, lambda p: parser.read_csv(p, index_col=0), temp_file
    )
    tm.assert_frame_equal(df, result)

