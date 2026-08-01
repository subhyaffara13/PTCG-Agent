
def test_parse_bool(all_parsers, data, kwargs, expected):
    parser = all_parsers
    result = parser.read_csv(StringIO(data), **kwargs)
    expected = DataFrame(expected, columns=["A", "B"])
    tm.assert_frame_equal(result, expected)

