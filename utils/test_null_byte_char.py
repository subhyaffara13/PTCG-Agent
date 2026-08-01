
def test_null_byte_char(request, all_parsers):
    # see gh-2741
    data = "\x00,foo"
    names = ["a", "b"]
    parser = all_parsers

    if parser.engine in ["c", "python"]:
        if parser.engine == "python":
            request.applymarker(
                pytest.mark.xfail(reason="This is read as an empty character not null")
            )
        expected = DataFrame([[np.nan, "foo"]], columns=names)
        out = parser.read_csv(StringIO(data), names=names)
        tm.assert_frame_equal(out, expected)
    else:
        if parser.engine == "pyarrow":
            # CSV parse error: Empty CSV file or block: "
            # cannot infer number of columns"
            pytest.skip(reason="https://github.com/apache/arrow/issues/38676")
        else:
            msg = "NULL byte detected"
        with pytest.raises(ParserError, match=msg):
            parser.read_csv(StringIO(data), names=names)

