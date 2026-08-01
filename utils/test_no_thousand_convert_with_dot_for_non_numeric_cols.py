
def test_no_thousand_convert_with_dot_for_non_numeric_cols(python_parser_only, dtype):
    # GH#50270
    parser = python_parser_only
    data = """\
a;b;c
0000.7995;16.000;0
3.03.001.00514;0;4.000
4923.600.041;23.000;131"""
    result = parser.read_csv(
        StringIO(data),
        sep=";",
        dtype=dtype,
        thousands=".",
    )
    expected = DataFrame(
        {
            "a": ["0000.7995", "3.03.001.00514", "4923.600.041"],
            "b": [16000, 0, 23000],
            "c": [0, 4000, 131],
        }
    )
    if dtype["a"] == object:
        expected["a"] = expected["a"].astype(object)
    tm.assert_frame_equal(result, expected)

