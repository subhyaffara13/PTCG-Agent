
def test_large_exponent(all_parsers_all_precisions, value, expected_value):
    # GH#38753; GH#38794; GH#62740
    parser, precision = all_parsers_all_precisions

    data = f"data\n{value}"
    result = parser.read_csv(StringIO(data), float_precision=precision)
    expected = DataFrame({"data": [expected_value]})
    tm.assert_frame_equal(result, expected)

