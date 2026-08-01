
def test_on_bad_lines_callable_not_expected_length(python_parser_only):
    # GH 5686
    parser = python_parser_only
    data = """a,b
1,2
2,3,4,5,6
3,4
"""
    bad_sio = StringIO(data)

    result = parser.read_csv_check_warnings(
        ParserWarning, "from bad_lines callable", bad_sio, on_bad_lines=lambda x: x
    )
    expected = DataFrame({"a": [1, 2, 3], "b": [2, 3, 4]})
    tm.assert_frame_equal(result, expected)

