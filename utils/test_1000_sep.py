
def test_1000_sep(all_parsers, number_csv, expected_number, request):
    parser = all_parsers
    data = f"""A|B|C
1|{number_csv}|5
10|13|10.
"""
    expected = DataFrame({"A": [1, 10], "B": [expected_number, 13], "C": [5, 10.0]})

    if parser.engine == "pyarrow":
        msg = "The 'thousands' option is not supported with the 'pyarrow' engine"
        with pytest.raises(ValueError, match=msg):
            parser.read_csv(StringIO(data), sep="|", thousands=",")
        return
    elif parser.engine == "python" and ",," in number_csv:
        mark = pytest.mark.xfail(
            reason="Python engine doesn't allow consecutive thousands separators"
        )
        request.applymarker(mark)

    result = parser.read_csv(StringIO(data), sep="|", thousands=",")
    tm.assert_frame_equal(result, expected)

