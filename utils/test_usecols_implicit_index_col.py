
def test_usecols_implicit_index_col(all_parsers):
    # see gh-2654
    parser = all_parsers
    data = "a,b,c\n4,apple,bat,5.7\n8,orange,cow,10"

    result = parser.read_csv(StringIO(data), usecols=["a", "b"])
    expected = DataFrame({"a": ["apple", "orange"], "b": ["bat", "cow"]}, index=[4, 8])
    tm.assert_frame_equal(result, expected)

