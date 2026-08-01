
def test_skip_rows_callable(all_parsers, kwargs, expected):
    parser = all_parsers
    data = "a\n1\n2\n3\n4\n5"

    result = parser.read_csv(StringIO(data), skiprows=lambda x: x % 2 == 0, **kwargs)
    expected = DataFrame({expected: [3, 5]})
    tm.assert_frame_equal(result, expected)

