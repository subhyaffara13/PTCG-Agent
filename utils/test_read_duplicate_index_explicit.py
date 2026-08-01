
def test_read_duplicate_index_explicit(all_parsers):
    data = """index,A,B,C,D
foo,2,3,4,5
bar,7,8,9,10
baz,12,13,14,15
qux,12,13,14,15
foo,12,13,14,15
bar,12,13,14,15
"""
    parser = all_parsers
    result = parser.read_csv(StringIO(data), index_col=0)

    expected = DataFrame(
        [
            [2, 3, 4, 5],
            [7, 8, 9, 10],
            [12, 13, 14, 15],
            [12, 13, 14, 15],
            [12, 13, 14, 15],
            [12, 13, 14, 15],
        ],
        columns=["A", "B", "C", "D"],
        index=Index(["foo", "bar", "baz", "qux", "foo", "bar"], name="index"),
    )
    tm.assert_frame_equal(result, expected)

