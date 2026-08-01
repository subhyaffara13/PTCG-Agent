
def test_converter_identity_object(all_parsers):
    # GH#40589
    parser = all_parsers
    data = "A,B\n1,2\n3,4"

    if parser.engine == "pyarrow":
        msg = "The 'converters' option is not supported with the 'pyarrow' engine"
        with pytest.raises(ValueError, match=msg):
            parser.read_csv(StringIO(data), converters={"A": lambda x: x})
        return

    rs = parser.read_csv(StringIO(data), converters={"A": lambda x: x})

    xp = DataFrame({"A": ["1", "3"], "B": [2, 4]})
    tm.assert_frame_equal(rs, xp)

