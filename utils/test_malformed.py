
def test_malformed(all_parsers):
    # see gh-6607
    parser = all_parsers
    data = """ignore
A,B,C
1,2,3 # comment
1,2,3,4,5
2,3,4
"""
    msg = "Expected 3 fields in line 4, saw 5"
    err = ParserError
    if parser.engine == "pyarrow":
        msg = "The 'comment' option is not supported with the 'pyarrow' engine"
        err = ValueError
    with pytest.raises(err, match=msg):
        parser.read_csv(StringIO(data), header=1, comment="#")

