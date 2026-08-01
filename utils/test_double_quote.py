
def test_double_quote(all_parsers, doublequote, exp_data, request):
    parser = all_parsers
    data = 'a,b\n3,"4 "" 5"'

    if parser.engine == "pyarrow" and not doublequote:
        mark = pytest.mark.xfail(reason="Mismatched result")
        request.applymarker(mark)

    result = parser.read_csv(StringIO(data), quotechar='"', doublequote=doublequote)
    expected = DataFrame(exp_data, columns=["a", "b"])
    tm.assert_frame_equal(result, expected)

