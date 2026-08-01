
def test_null_quote_char(all_parsers, quoting, quote_char):
    kwargs = {"quotechar": quote_char, "quoting": quoting}
    data = "a,b,c\n1,2,3"
    parser = all_parsers

    if quoting != csv.QUOTE_NONE:
        # Sanity checking.
        if not PY314:
            msg = "1-character string"
        else:
            msg = "unicode character or None"
        msg = (
            f'"quotechar" must be a {msg}'
            if all_parsers.engine == "python" and quote_char == ""
            else "quotechar must be set if quoting enabled"
        )

        with pytest.raises(TypeError, match=msg):
            parser.read_csv(StringIO(data), **kwargs)
    elif all_parsers.engine != "python":
        # Python doesn't support null/blank quote chars in their csv parsers
        expected = DataFrame([[1, 2, 3]], columns=["a", "b", "c"])
        result = parser.read_csv(StringIO(data), **kwargs)
        tm.assert_frame_equal(result, expected)

