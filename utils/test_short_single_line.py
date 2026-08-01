
def test_short_single_line(all_parsers):
    # GH 47566
    parser = all_parsers
    columns = ["a", "b", "c"]
    data = "1,2"
    result = parser.read_csv(StringIO(data), header=None, names=columns)
    expected = DataFrame({"a": [1], "b": [2], "c": [np.nan]})
    tm.assert_frame_equal(result, expected)

