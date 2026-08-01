
def test_read_nrows_bad(all_parsers, nrows):
    data = """index,A,B,C,D
foo,2,3,4,5
bar,7,8,9,10
baz,12,13,14,15
qux,12,13,14,15
foo2,12,13,14,15
bar2,12,13,14,15
"""
    msg = r"'nrows' must be an integer >=0"
    parser = all_parsers
    if parser.engine == "pyarrow":
        msg = "The 'nrows' option is not supported with the 'pyarrow' engine"

    with pytest.raises(ValueError, match=msg):
        parser.read_csv(StringIO(data), nrows=nrows)

