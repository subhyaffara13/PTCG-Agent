
def test_converters_no_implicit_conv(all_parsers):
    # see gh-2184
    parser = all_parsers
    data = """000102,1.2,A\n001245,2,B"""

    converters = {0: lambda x: x.strip()}

    if parser.engine == "pyarrow":
        msg = "The 'converters' option is not supported with the 'pyarrow' engine"
        with pytest.raises(ValueError, match=msg):
            parser.read_csv(StringIO(data), header=None, converters=converters)
        return

    result = parser.read_csv(StringIO(data), header=None, converters=converters)

    # Column 0 should not be casted to numeric and should remain as object.
    expected = DataFrame([["000102", 1.2, "A"], ["001245", 2, "B"]])
    tm.assert_frame_equal(result, expected)

