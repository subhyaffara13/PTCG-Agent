
def test_usecols_regex_sep(all_parsers):
    # see gh-2733
    parser = all_parsers
    data = "a  b  c\n4  apple  bat  5.7\n8  orange  cow  10"

    if parser.engine == "pyarrow":
        msg = "the 'pyarrow' engine does not support regex separators"
        with pytest.raises(ValueError, match=msg):
            parser.read_csv(StringIO(data), sep=r"\s+", usecols=("a", "b"))
        return

    result = parser.read_csv(StringIO(data), sep=r"\s+", usecols=("a", "b"))

    expected = DataFrame({"a": ["apple", "orange"], "b": ["bat", "cow"]}, index=[4, 8])
    tm.assert_frame_equal(result, expected)

