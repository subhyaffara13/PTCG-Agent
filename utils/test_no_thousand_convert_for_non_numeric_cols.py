
def test_no_thousand_convert_for_non_numeric_cols(python_parser_only, dtype, expected):
    # GH#50270
    parser = python_parser_only
    data = """a;b;c
0000,7995;16,000.1;0
3,03,001,00514;0;4,001
4923,600,041;23,000;131
"""
    result = parser.read_csv(
        StringIO(data),
        sep=";",
        dtype=dtype,
        thousands=",",
    )
    expected = DataFrame(expected)
    expected.insert(0, "a", ["0000,7995", "3,03,001,00514", "4923,600,041"])
    tm.assert_frame_equal(result, expected)

