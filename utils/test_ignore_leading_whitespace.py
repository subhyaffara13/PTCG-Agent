
def test_ignore_leading_whitespace(all_parsers):
    # see gh-3374, gh-6607
    parser = all_parsers
    data = " a b c\n 1 2 3\n 4 5 6\n 7 8 9"

    if parser.engine == "pyarrow":
        msg = "the 'pyarrow' engine does not support regex separators"
        with pytest.raises(ValueError, match=msg):
            parser.read_csv(StringIO(data), sep=r"\s+")
        return
    result = parser.read_csv(StringIO(data), sep=r"\s+")

    expected = DataFrame({"a": [1, 4, 7], "b": [2, 5, 8], "c": [3, 6, 9]})
    tm.assert_frame_equal(result, expected)

