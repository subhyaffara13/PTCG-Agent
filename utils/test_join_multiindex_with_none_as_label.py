
def test_join_multiindex_with_none_as_label():
    # GH 58721
    df1 = DataFrame(
        {"A": [1]},
        index=MultiIndex.from_tuples([(3, 3)], names=["X", None]),
    )
    df2 = DataFrame(
        {"B": [2]},
        index=MultiIndex.from_tuples([(3, 3)], names=[None, "X"]),
    )

    result12 = df1.join(df2)
    expected12 = DataFrame(
        {"A": [1], "B": [2]},
        index=MultiIndex.from_tuples([(3, 3)], names=["X", None]),
    )
    tm.assert_frame_equal(result12, expected12)

    result21 = df2.join(df1)
    expected21 = DataFrame(
        {"B": [2], "A": [1]},
        index=MultiIndex.from_tuples([(3, 3)], names=[None, "X"]),
    )
    tm.assert_frame_equal(result21, expected21)

