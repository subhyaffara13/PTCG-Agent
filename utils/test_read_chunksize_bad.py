
def test_read_chunksize_bad(all_parsers, chunksize):
    data = """index,A,B,C,D
foo,2,3,4,5
bar,7,8,9,10
baz,12,13,14,15
qux,12,13,14,15
foo2,12,13,14,15
bar2,12,13,14,15
"""
    parser = all_parsers
    msg = r"'chunksize' must be an integer >=1"
    if parser.engine == "pyarrow":
        msg = "The 'chunksize' option is not supported with the 'pyarrow' engine"

    with pytest.raises(ValueError, match=msg):
        with parser.read_csv(StringIO(data), chunksize=chunksize) as _:
            pass

