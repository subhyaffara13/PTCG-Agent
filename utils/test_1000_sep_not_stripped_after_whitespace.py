
def test_1000_sep_not_stripped_after_whitespace(all_parsers, value):
    parser = all_parsers
    data = f"a\n{value}\n"
    expected = DataFrame({"a": [value]})

    if parser.engine == "pyarrow":
        msg = "The 'thousands' option is not supported with the 'pyarrow' engine"
        with pytest.raises(ValueError, match=msg):
            parser.read_csv(StringIO(data), sep=";", thousands=",")
        return

    result = parser.read_csv(StringIO(data), sep=";", thousands=",")
    tm.assert_frame_equal(result, expected)

