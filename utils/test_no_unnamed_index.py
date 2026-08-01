
def test_no_unnamed_index(all_parsers):
    parser = all_parsers
    data = """ id c0 c1 c2
0 1 0 a b
1 2 0 c d
2 2 2 e f
"""
    result = parser.read_csv(StringIO(data), sep=" ")
    expected = DataFrame(
        [[0, 1, 0, "a", "b"], [1, 2, 0, "c", "d"], [2, 2, 2, "e", "f"]],
        columns=["Unnamed: 0", "id", "c0", "c1", "c2"],
    )
    tm.assert_frame_equal(result, expected)

