
def test_pickle_buffer_roundtrip(temp_file):
    path = temp_file
    df = DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=Index(list("ABCD"), dtype=object),
        index=Index([f"i-{i}" for i in range(30)], dtype=object),
    )
    with open(path, "wb") as fh:
        df.to_pickle(fh)
    with open(path, "rb") as fh:
        result = pd.read_pickle(fh)
    tm.assert_frame_equal(df, result)

