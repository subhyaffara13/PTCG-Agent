
def test_converters(all_parsers, column, converter):
    parser = all_parsers
    data = """A,B,C,D
a,1,2,01/01/2009
b,3,4,01/02/2009
c,4,5,01/03/2009
"""
    if parser.engine == "pyarrow":
        msg = "The 'converters' option is not supported with the 'pyarrow' engine"
        with pytest.raises(ValueError, match=msg):
            parser.read_csv(StringIO(data), converters={column: converter})
        return

    result = parser.read_csv(StringIO(data), converters={column: converter})

    expected = parser.read_csv(StringIO(data))
    expected["D"] = expected["D"].map(converter)

    tm.assert_frame_equal(result, expected)

