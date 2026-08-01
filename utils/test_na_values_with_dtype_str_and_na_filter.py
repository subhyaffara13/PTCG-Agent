
def test_na_values_with_dtype_str_and_na_filter(
    all_parsers, na_filter, using_infer_string, request
):
    # see gh-20377
    parser = all_parsers
    if parser.engine == "pyarrow" and (na_filter is False or not using_infer_string):
        mark = pytest.mark.xfail(reason="mismatched shape")
        request.applymarker(mark)

    data = "a,b,c\n1,,3\n4,5,6"

    # na_filter=True --> missing value becomes NaN.
    # na_filter=False --> missing value remains empty string.
    empty = np.nan if na_filter else ""
    expected = DataFrame({"a": ["1", "4"], "b": [empty, "5"], "c": ["3", "6"]})

    result = parser.read_csv(StringIO(data), na_filter=na_filter, dtype=str)
    tm.assert_frame_equal(result, expected)

