
def test_no_header(all_parsers, kwargs, names):
    parser = all_parsers
    data = """1,2,3,4,5
6,7,8,9,10
11,12,13,14,15
"""
    expected = DataFrame(
        [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15]], columns=names
    )
    result = parser.read_csv(StringIO(data), header=None, **kwargs)
    tm.assert_frame_equal(result, expected)

