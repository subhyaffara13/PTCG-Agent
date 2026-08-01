
def test_on_bad_lines_callable_iterator_true(python_parser_only, bad_line_func, sep):
    # GH 5686
    # iterator=True has a separate code path than iterator=False
    parser = python_parser_only
    data = f"""
0{sep}1
hi{sep}there
foo{sep}bar{sep}baz
good{sep}bye
"""
    bad_sio = StringIO(data)
    result_iter = parser.read_csv(
        bad_sio, on_bad_lines=bad_line_func, chunksize=1, iterator=True, sep=sep
    )
    expecteds = [
        {"0": "hi", "1": "there"},
        {"0": "foo", "1": "bar"},
        {"0": "good", "1": "bye"},
    ]
    for i, (result, expected) in enumerate(zip(result_iter, expecteds)):
        expected = DataFrame(expected, index=range(i, i + 1))
        tm.assert_frame_equal(result, expected)

