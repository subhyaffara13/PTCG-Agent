
def test_error_bad_lines(all_parsers):
    # see gh-15925
    parser = all_parsers
    data = "a\n1\n1,2,3\n4\n5,6,7"

    msg = "Expected 1 fields in line 3, saw 3"

    if parser.engine == "pyarrow":
        # "CSV parse error: Expected 1 columns, got 3: 1,2,3"
        pytest.skip(reason="https://github.com/apache/arrow/issues/38676")

    with pytest.raises(ParserError, match=msg):
        parser.read_csv(StringIO(data), on_bad_lines="error")

