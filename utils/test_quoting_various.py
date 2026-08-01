
def test_quoting_various(all_parsers, kwargs, exp_data):
    data = '1,2,"foo"'
    parser = all_parsers
    columns = ["a", "b", "c"]

    result = parser.read_csv(StringIO(data), names=columns, **kwargs)
    expected = DataFrame(exp_data, columns=columns)
    tm.assert_frame_equal(result, expected)

