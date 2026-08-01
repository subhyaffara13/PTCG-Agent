
def test_outside_int64_uint64_range_follow_str(all_parsers, val):
    parser = all_parsers

    result = parser.read_csv(StringIO(f"{val}\nabc"), header=None)

    expected = DataFrame([str(val), "abc"])
    tm.assert_frame_equal(result, expected)

