
def test_parse_ragged_csv(c_parser_only):
    parser = c_parser_only
    data = """1,2,3
1,2,3,4
1,2,3,4,5
1,2
1,2,3,4"""

    nice_data = """1,2,3,,
1,2,3,4,
1,2,3,4,5
1,2,,,
1,2,3,4,"""
    result = parser.read_csv(
        StringIO(data), header=None, names=["a", "b", "c", "d", "e"]
    )

    expected = parser.read_csv(
        StringIO(nice_data), header=None, names=["a", "b", "c", "d", "e"]
    )

    tm.assert_frame_equal(result, expected)

    # too many columns, cause segfault if not careful
    data = "1,2\n3,4,5"

    result = parser.read_csv(StringIO(data), header=None, names=range(50))
    expected = parser.read_csv(StringIO(data), header=None, names=range(3)).reindex(
        columns=range(50)
    )

    tm.assert_frame_equal(result, expected)

