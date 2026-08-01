
def test_usecols_with_whitespace(all_parsers):
    parser = all_parsers
    data = "a  b  c\n4  apple  bat  5.7\n8  orange  cow  10"

    result = parser.read_csv(StringIO(data), sep=r"\s+", usecols=("a", "b"))
    expected = DataFrame({"a": ["apple", "orange"], "b": ["bat", "cow"]}, index=[4, 8])
    tm.assert_frame_equal(result, expected)

