
def test_header_with_index_col(all_parsers):
    parser = all_parsers
    data = """foo,1,2,3
bar,4,5,6
baz,7,8,9
"""
    names = ["A", "B", "C"]
    result = parser.read_csv(StringIO(data), names=names)

    expected = DataFrame(
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        index=["foo", "bar", "baz"],
        columns=["A", "B", "C"],
    )
    tm.assert_frame_equal(result, expected)


def test_header_with_index_col(all_parsers):
    # GH 33476
    parser = all_parsers
    data = """
I11,A,A
I12,B,B
I2,1,3
"""
    midx = MultiIndex.from_tuples([("A", "B"), ("A", "B.1")], names=["I11", "I12"])
    idx = Index(["I2"])
    expected = DataFrame([[1, 3]], index=idx, columns=midx)

    result = parser.read_csv(StringIO(data), index_col=0, header=[0, 1])
    tm.assert_frame_equal(result, expected)

    col_idx = Index(["A", "A.1"])
    idx = Index(["I12", "I2"], name="I11")
    expected = DataFrame([["B", "B"], ["1", "3"]], index=idx, columns=col_idx)

    result = parser.read_csv(StringIO(data), index_col="I11", header=0)
    tm.assert_frame_equal(result, expected)

