
def test_encoding_surrogatepass(all_parsers, tmp_path):
    # GH39017
    parser = all_parsers
    content = b"\xed\xbd\xbf"
    decoded = content.decode("utf-8", errors="surrogatepass")
    expected = DataFrame({decoded: [decoded]}, index=[decoded * 2])
    expected.index.name = decoded * 2

    path = tmp_path / "test_encoding.csv"
    path.write_bytes(
        content * 2 + b"," + content + b"\n" + content * 2 + b"," + content
    )
    df = parser.read_csv(path, encoding_errors="surrogatepass", index_col=0)
    tm.assert_frame_equal(df, expected)
    with pytest.raises(UnicodeDecodeError, match="'utf-8' codec can't decode byte"):
        parser.read_csv(path)

