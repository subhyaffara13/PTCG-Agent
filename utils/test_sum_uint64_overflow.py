
def test_sum_uint64_overflow():
    # see gh-14758
    # Convert to uint64 and don't overflow
    df = DataFrame([[1, 2], [3, 4], [5, 6]], dtype=object)
    df = df + 9223372036854775807

    index = Index(
        [9223372036854775808, 9223372036854775810, 9223372036854775812], dtype=np.uint64
    )
    expected = DataFrame(
        {1: [9223372036854775809, 9223372036854775811, 9223372036854775813]},
        index=index,
        dtype=object,
    )

    expected.index.name = 0
    result = df.groupby(0).sum(numeric_only=False)
    tm.assert_frame_equal(result, expected)

    # out column is non-numeric, so with numeric_only=True it is dropped
    result2 = df.groupby(0).sum(numeric_only=True)
    expected2 = expected[[]]
    tm.assert_frame_equal(result2, expected2)

