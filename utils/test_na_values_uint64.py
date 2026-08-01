
def test_na_values_uint64(all_parsers, data, kwargs, expected, request):
    # see gh-14983
    parser = all_parsers

    if parser.engine == "pyarrow" and "na_values" in kwargs:
        msg = "The 'pyarrow' engine requires all na_values to be strings"
        with pytest.raises(TypeError, match=msg):
            parser.read_csv(StringIO(data), header=None, **kwargs)
        return
    elif parser.engine == "pyarrow":
        mark = pytest.mark.xfail(reason="Returns float64 instead of object")
        request.applymarker(mark)

    result = parser.read_csv(StringIO(data), header=None, **kwargs)
    expected = DataFrame(expected)
    tm.assert_frame_equal(result, expected)

