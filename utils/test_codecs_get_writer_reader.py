
def test_codecs_get_writer_reader(temp_file):
    # GH39247
    expected = pd.DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=pd.Index(list("ABCD")),
        index=pd.Index([f"i-{i}" for i in range(30)]),
    )
    with open(temp_file, "wb") as handle:
        with codecs.getwriter("utf-8")(handle) as encoded:
            expected.to_csv(encoded)
    with open(temp_file, "rb") as handle:
        with codecs.getreader("utf-8")(handle) as encoded:
            df = pd.read_csv(encoded, index_col=0)
    tm.assert_frame_equal(expected, df)

