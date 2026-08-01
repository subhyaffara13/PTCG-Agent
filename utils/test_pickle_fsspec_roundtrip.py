
def test_pickle_fsspec_roundtrip(temp_file):
    pytest.importorskip("fsspec")
    # Using temp_file for context, but fsspec uses memory URL
    mockurl = "memory://mockfile"
    df = DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=Index(list("ABCD"), dtype=object),
        index=Index([f"i-{i}" for i in range(30)], dtype=object),
    )
    df.to_pickle(mockurl)
    result = pd.read_pickle(mockurl)
    tm.assert_frame_equal(df, result)

