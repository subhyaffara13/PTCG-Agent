
def test_skipfooter(python_parser_only, kwargs):
    # see gh-6607
    data = """A,B,C
1,2,3
4,5,6
7,8,9
want to skip this
also also skip this
"""
    parser = python_parser_only
    result = parser.read_csv(StringIO(data), **kwargs)

    expected = DataFrame([[1, 2, 3], [4, 5, 6], [7, 8, 9]], columns=["A", "B", "C"])
    tm.assert_frame_equal(result, expected)

