
def test_to_csv_iterative_compression_name(compression, temp_file):
    # GH 38714
    df = DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=Index(list("ABCD")),
        index=Index([f"i-{i}" for i in range(30)]),
    )
    df.to_csv(temp_file, compression=compression, chunksize=1)
    tm.assert_frame_equal(
        pd.read_csv(temp_file, compression=compression, index_col=0), df
    )

