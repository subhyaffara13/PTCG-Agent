
def test_range_difference(start1, stop1, step1, start2, stop2, step2):
    # test that
    #  a) we match Index[int64].difference and
    #  b) we return RangeIndex whenever it is possible to do so.
    assume(step1 != 0)
    assume(step2 != 0)

    left = RangeIndex(start1, stop1, step1)
    right = RangeIndex(start2, stop2, step2)

    result = left.difference(right, sort=None)
    assert_range_or_not_is_rangelike(result)

    left_int64 = Index(left.to_numpy())
    right_int64 = Index(right.to_numpy())

    alt = left_int64.difference(right_int64, sort=None)
    tm.assert_index_equal(result, alt, exact="equiv")

    result = left.difference(right, sort=False)
    assert_range_or_not_is_rangelike(result)

    alt = left_int64.difference(right_int64, sort=False)
    tm.assert_index_equal(result, alt, exact="equiv")

