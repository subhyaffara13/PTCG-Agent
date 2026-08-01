
def test_infer_index_col(all_parsers):
    data = """A,B,C
foo,1,2,3
bar,4,5,6
baz,7,8,9
"""
    parser = all_parsers
    result = parser.read_csv(StringIO(data))

    expected = DataFrame(
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        index=["foo", "bar", "baz"],
        columns=["A", "B", "C"],
    )
    tm.assert_frame_equal(result, expected)

