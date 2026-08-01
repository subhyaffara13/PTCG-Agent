
def test_on_bad_lines_warn_correct_formatting(all_parsers):
    # see gh-15925
    parser = all_parsers
    data = """1,2
a,b
a,b,c
a,b,d
a,b
"""
    expected = DataFrame({"1": "a", "2": ["b"] * 2})
    match_msg = "Skipping line"

    expected_warning = ParserWarning
    if parser.engine == "pyarrow":
        match_msg = "Expected 2 columns, but found 3: a,b,c"

    with tm.assert_produces_warning(
        expected_warning, match=match_msg, check_stacklevel=False
    ):
        result = parser.read_csv(StringIO(data), on_bad_lines="warn")
    tm.assert_frame_equal(result, expected)

