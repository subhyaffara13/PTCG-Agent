
def test_invalid_float_number(all_parsers_all_precisions, value):
    # GH#62617
    parser, precision = all_parsers_all_precisions
    data = f"h1,h2,h3\ndata1,{value},data3"

    result = parser.read_csv(StringIO(data), float_precision=precision)
    expected = DataFrame({"h1": ["data1"], "h2": [value], "h3": "data3"})
    tm.assert_frame_equal(result, expected)

