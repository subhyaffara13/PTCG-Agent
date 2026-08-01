
def test_malformed_chunks(all_parsers, nrows):
    data = """ignore
A,B,C
skip
1,2,3
3,5,10 # comment
1,2,3,4,5
2,3,4
"""
    parser = all_parsers

    if parser.engine == "pyarrow":
        msg = "The 'iterator' option is not supported with the 'pyarrow' engine"
        with pytest.raises(ValueError, match=msg):
            parser.read_csv(
                StringIO(data),
                header=1,
                comment="#",
                iterator=True,
                chunksize=1,
                skiprows=[2],
            )
        return

    msg = "Expected 3 fields in line 6, saw 5"
    with parser.read_csv(
        StringIO(data), header=1, comment="#", iterator=True, chunksize=1, skiprows=[2]
    ) as reader:
        with pytest.raises(ParserError, match=msg):
            reader.read(nrows)

