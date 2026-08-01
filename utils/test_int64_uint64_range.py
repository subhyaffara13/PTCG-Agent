
def test_int64_uint64_range(all_parsers, val):
    # These numbers fall right inside the int64-uint64
    # range, so they should be parsed as integer.
    parser = all_parsers
    result = parser.read_csv(StringIO(str(val)), header=None)

    expected = DataFrame([val])
    tm.assert_frame_equal(result, expected)

