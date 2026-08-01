
def test_non_string_na_values(all_parsers, data, na_values, request):
    # see gh-3611: with an odd float format, we can't match
    # the string "999.0" exactly but still need float matching
    parser = all_parsers
    expected = DataFrame([[np.nan, 1.2], [2.0, np.nan], [3.0, 4.5]], columns=["A", "B"])

    if parser.engine == "pyarrow" and not all(isinstance(x, str) for x in na_values):
        msg = "The 'pyarrow' engine requires all na_values to be strings"
        with pytest.raises(TypeError, match=msg):
            parser.read_csv(StringIO(data), na_values=na_values)
        return
    elif parser.engine == "pyarrow" and "-999.000" in data:
        # bc the pyarrow engine does not include the float-ified version
        #  of "-999" -> -999, it does not match the entry with the trailing
        #  zeros, so "-999.000" is not treated as null.
        mark = pytest.mark.xfail(
            reason="pyarrow engined does not recognize equivalent floats"
        )
        request.applymarker(mark)

    result = parser.read_csv(StringIO(data), na_values=na_values)
    tm.assert_frame_equal(result, expected)

