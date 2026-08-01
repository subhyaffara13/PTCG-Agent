
def test_header_names_backward_compat(all_parsers, data, header, request):
    # see gh-2539
    parser = all_parsers

    if parser.engine == "pyarrow" and header is not None:
        mark = pytest.mark.xfail(reason="DataFrame.columns are different")
        request.applymarker(mark)

    expected = parser.read_csv(StringIO("1,2,3\n4,5,6"), names=["a", "b", "c"])

    result = parser.read_csv(StringIO(data), names=["a", "b", "c"], header=header)
    tm.assert_frame_equal(result, expected)

