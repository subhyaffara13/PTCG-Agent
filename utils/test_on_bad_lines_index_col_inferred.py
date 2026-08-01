
def test_on_bad_lines_index_col_inferred(python_parser_only):
    # GH 5686
    parser = python_parser_only
    data = """a,b
1,2,3
4,5,6
"""
    bad_sio = StringIO(data)

    result = parser.read_csv(bad_sio, on_bad_lines=lambda x: ["99", "99"])
    expected = DataFrame({"a": [2, 5], "b": [3, 6]}, index=[1, 4])
    tm.assert_frame_equal(result, expected)

