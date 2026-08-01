
def test_read_chunksize_compat(all_parsers, kwargs):
    # see gh-12185
    data = """index,A,B,C,D
foo,2,3,4,5
bar,7,8,9,10
baz,12,13,14,15
qux,12,13,14,15
foo2,12,13,14,15
bar2,12,13,14,15
"""
    parser = all_parsers
    result = parser.read_csv(StringIO(data), **kwargs)

    if parser.engine == "pyarrow":
        msg = "The 'chunksize' option is not supported with the 'pyarrow' engine"
        with pytest.raises(ValueError, match=msg):
            with parser.read_csv(StringIO(data), chunksize=2, **kwargs) as reader:
                concat(reader)
        return

    with parser.read_csv(StringIO(data), chunksize=2, **kwargs) as reader:
        via_reader = concat(reader)
    tm.assert_frame_equal(via_reader, result)

