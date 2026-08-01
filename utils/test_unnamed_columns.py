
def test_unnamed_columns(all_parsers):
    data = """A,B,C,,
1,2,3,4,5
6,7,8,9,10
11,12,13,14,15
"""
    parser = all_parsers
    expected = DataFrame(
        [[1, 2, 3, 4, 5], [6, 7, 8, 9, 10], [11, 12, 13, 14, 15]],
        dtype=np.int64,
        columns=["A", "B", "C", "Unnamed: 3", "Unnamed: 4"],
    )
    result = parser.read_csv(StringIO(data))
    tm.assert_frame_equal(result, expected)

