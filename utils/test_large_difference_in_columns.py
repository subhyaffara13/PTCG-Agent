
def test_large_difference_in_columns(c_parser_only):
    # see gh-14125
    parser = c_parser_only

    count = 10000
    large_row = ("X," * count)[:-1] + "\n"
    normal_row = "XXXXXX XXXXXX,111111111111111\n"
    test_input = (large_row + normal_row * 6)[:-1]

    result = parser.read_csv(StringIO(test_input), header=None, usecols=[0])
    rows = test_input.split("\n")

    expected = DataFrame([row.split(",")[0] for row in rows])
    tm.assert_frame_equal(result, expected)

