
def test_nrows_iterator_without_chunksize(all_parsers):
    # GH 59079
    parser = all_parsers
    data = """A,B,C
foo,1,2,3
bar,4,5,6
baz,7,8,9
"""
    if parser.engine == "pyarrow":
        msg = "The 'iterator' option is not supported with the 'pyarrow' engine"
        with pytest.raises(ValueError, match=msg):
            parser.read_csv(StringIO(data), iterator=True, nrows=2)
        return

    with parser.read_csv(StringIO(data), iterator=True, nrows=2) as reader:
        result = reader.get_chunk()

    expected = DataFrame(
        [[1, 2, 3], [4, 5, 6]],
        index=["foo", "bar"],
        columns=["A", "B", "C"],
    )
    tm.assert_frame_equal(result, expected)

