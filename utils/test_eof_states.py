
def test_eof_states(all_parsers, data, kwargs, expected, msg, request):
    # see gh-10728, gh-10548
    parser = all_parsers

    if parser.engine == "pyarrow" and "comment" in kwargs:
        msg = "The 'comment' option is not supported with the 'pyarrow' engine"
        with pytest.raises(ValueError, match=msg):
            parser.read_csv(StringIO(data), **kwargs)
        return

    if parser.engine == "pyarrow" and "\r" not in data:
        # pandas.errors.ParserError: CSV parse error: Expected 3 columns, got 1:
        # ValueError: skiprows argument must be an integer when using engine='pyarrow'
        # AssertionError: Regex pattern did not match.
        pytest.skip(reason="https://github.com/apache/arrow/issues/38676")

    if expected is None:
        with pytest.raises(ParserError, match=msg):
            parser.read_csv(StringIO(data), **kwargs)
    else:
        result = parser.read_csv(StringIO(data), **kwargs)
        tm.assert_frame_equal(result, expected)

