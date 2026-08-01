
def test_converters_type_must_be_dict(all_parsers):
    parser = all_parsers
    data = """index,A,B,C,D
foo,2,3,4,5
"""
    if parser.engine == "pyarrow":
        msg = "The 'converters' option is not supported with the 'pyarrow' engine"
        with pytest.raises(ValueError, match=msg):
            parser.read_csv(StringIO(data), converters=0)
        return
    with pytest.raises(TypeError, match="Type converters.+"):
        parser.read_csv(StringIO(data), converters=0)

