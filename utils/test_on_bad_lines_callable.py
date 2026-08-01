
def test_on_bad_lines_callable(python_parser_only, bad_line_func):
    # GH 5686
    parser = python_parser_only
    data = """a,b
1,2
2,3,4,5,6
3,4
"""
    bad_sio = StringIO(data)
    result = parser.read_csv(bad_sio, on_bad_lines=bad_line_func)
    expected = DataFrame({"a": [1, 2, 3], "b": [2, 3, 4]})
    tm.assert_frame_equal(result, expected)

