
def test_reader_list_skiprows(all_parsers):
    data = """index,A,B,C,D
foo,2,3,4,5
bar,7,8,9,10
baz,12,13,14,15
qux,12,13,14,15
foo2,12,13,14,15
bar2,12,13,14,15
"""
    parser = all_parsers
    kwargs = {"index_col": 0}

    lines = list(csv.reader(StringIO(data)))
    with TextParser(lines, chunksize=2, skiprows=[1], **kwargs) as reader:
        chunks = list(reader)

    expected = parser.read_csv(StringIO(data), **kwargs)

    tm.assert_frame_equal(chunks[0], expected[1:3])

