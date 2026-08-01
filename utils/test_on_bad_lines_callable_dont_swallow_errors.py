
def test_on_bad_lines_callable_dont_swallow_errors(python_parser_only):
    # GH 5686
    parser = python_parser_only
    data = """a,b
1,2
2,3,4,5,6
3,4
"""
    bad_sio = StringIO(data)
    msg = "This function is buggy."

    def bad_line_func(bad_line):
        raise ValueError(msg)

    with pytest.raises(ValueError, match=msg):
        parser.read_csv(bad_sio, on_bad_lines=bad_line_func)

