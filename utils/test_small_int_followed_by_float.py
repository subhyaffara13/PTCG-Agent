
def test_small_int_followed_by_float(
    all_parsers_all_precisions, value, expected_value, request
):
    # GH#51295
    parser, precision = all_parsers_all_precisions
    data = f"""data
    42
    {value}"""
    result = parser.read_csv(StringIO(data), float_precision=precision)
    expected = DataFrame({"data": [42.0, expected_value]})

    tm.assert_frame_equal(result, expected)

