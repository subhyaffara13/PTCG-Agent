
def test_skip_rows_and_n_rows():
    # GH#44021
    data = """a\tb
1\t a
2\t b
3\t c
4\t d
5\t e
6\t f
    """
    result = read_fwf(StringIO(data), nrows=4, skiprows=[2, 4])
    expected = DataFrame({"a": [1, 3, 5, 6], "b": ["a", "c", "e", "f"]})
    tm.assert_frame_equal(result, expected)


def test_skip_rows_and_n_rows(all_parsers):
    # GH#44021
    data = """a,b
1,a
2,b
3,c
4,d
5,e
6,f
7,g
8,h
"""
    parser = all_parsers
    result = parser.read_csv(StringIO(data), nrows=5, skiprows=[2, 4, 6])
    expected = DataFrame({"a": [1, 3, 5, 7, 8], "b": ["a", "c", "e", "g", "h"]})
    tm.assert_frame_equal(result, expected)

