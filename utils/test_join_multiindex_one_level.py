
def test_join_multiindex_one_level(join_type):
    # GH#36909
    left = DataFrame(
        data={"c": 3}, index=MultiIndex.from_tuples([(1, 2)], names=("a", "b"))
    )
    right = DataFrame(data={"d": 4}, index=MultiIndex.from_tuples([(2,)], names=("b",)))
    result = left.join(right, how=join_type)
    if join_type == "right":
        expected = DataFrame(
            {"c": [3], "d": [4]},
            index=MultiIndex.from_tuples([(2, 1)], names=["b", "a"]),
        )
    else:
        expected = DataFrame(
            {"c": [3], "d": [4]},
            index=MultiIndex.from_tuples([(1, 2)], names=["a", "b"]),
        )
    tm.assert_frame_equal(result, expected)

