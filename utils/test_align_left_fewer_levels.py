
def test_align_left_fewer_levels():
    # GH#45224
    left = Series([2], index=pd.MultiIndex.from_tuples([(1, 3)], names=["a", "c"]))
    right = Series(
        [1], index=pd.MultiIndex.from_tuples([(1, 2, 3)], names=["a", "b", "c"])
    )
    result_left, result_right = left.align(right)

    expected_right = Series(
        [1], index=pd.MultiIndex.from_tuples([(1, 3, 2)], names=["a", "c", "b"])
    )
    expected_left = Series(
        [2], index=pd.MultiIndex.from_tuples([(1, 3, 2)], names=["a", "c", "b"])
    )
    tm.assert_series_equal(result_left, expected_left)
    tm.assert_series_equal(result_right, expected_right)

