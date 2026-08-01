
def test_float_parser(all_parsers):
    # see gh-9565
    parser = all_parsers
    data = "45e-1,4.5,45.,inf,-inf"
    result = parser.read_csv(StringIO(data), header=None)

    expected = DataFrame([[float(s) for s in data.split(",")]])
    tm.assert_frame_equal(result, expected)

