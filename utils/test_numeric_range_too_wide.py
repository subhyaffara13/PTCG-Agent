
def test_numeric_range_too_wide(all_parsers, exp_data):
    # No numerical dtype can hold both negative and uint64
    # values, so they should be cast as string.
    parser = all_parsers
    data = "\n".join(exp_data)
    expected = DataFrame(exp_data)

    result = parser.read_csv(StringIO(data), header=None)
    tm.assert_frame_equal(result, expected)

