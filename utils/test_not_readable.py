
def test_not_readable(all_parsers, mode):
    # GH43439
    parser = all_parsers
    content = b"abcd"
    if "t" in mode:
        content = "abcd"
    with tempfile.SpooledTemporaryFile(mode=mode, encoding="utf-8") as handle:
        handle.write(content)
        handle.seek(0)
        df = parser.read_csv(handle)
    expected = DataFrame([], columns=["abcd"])
    tm.assert_frame_equal(df, expected)

