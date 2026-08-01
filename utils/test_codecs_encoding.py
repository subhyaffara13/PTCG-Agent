
def test_codecs_encoding(format, temp_file):
    # GH39247
    expected = pd.DataFrame(
        1.1 * np.arange(120).reshape((30, 4)),
        columns=pd.Index(list("ABCD")),
        index=pd.Index([f"i-{i}" for i in range(30)]),
    )
    with open(temp_file, mode="w", encoding="utf-8") as handle:
        getattr(expected, f"to_{format}")(handle)
    with open(temp_file, encoding="utf-8") as handle:
        if format == "csv":
            df = pd.read_csv(handle, index_col=0)
        else:
            df = pd.read_json(handle)
    tm.assert_frame_equal(expected, df)

