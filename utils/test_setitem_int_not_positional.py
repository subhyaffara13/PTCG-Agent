
def test_setitem_int_not_positional():
    # GH#42215 deprecated falling back to positional on __setitem__ with an
    #  int not contained in the index; enforced in 2.0
    ser = Series([1, 2, 3, 4], index=[1.1, 2.1, 3.0, 4.1])
    assert not ser.index._should_fallback_to_positional
    # assert not ser.index.astype(object)._should_fallback_to_positional

    # 3.0 is in our index, so post-enforcement behavior is unchanged
    ser[3] = 10
    expected = Series([1, 2, 10, 4], index=ser.index)
    tm.assert_series_equal(ser, expected)

    # pre-enforcement `ser[5] = 5` raised IndexError
    ser[5] = 5
    expected = Series([1, 2, 10, 4, 5], index=[1.1, 2.1, 3.0, 4.1, 5.0])
    tm.assert_series_equal(ser, expected)

    ii = IntervalIndex.from_breaks(range(10))[::2]
    ser2 = Series(range(len(ii)), index=ii)
    exp_index = ii.astype(object).append(Index([4]))
    expected2 = Series([0, 1, 2, 3, 4, 9], index=exp_index)
    # pre-enforcement `ser2[4] = 9` interpreted 4 as positional
    ser2[4] = 9
    tm.assert_series_equal(ser2, expected2)

    mi = MultiIndex.from_product([ser.index, ["A", "B"]])
    ser3 = Series(range(len(mi)), index=mi)
    expected3 = ser3.copy()
    expected3.loc[4] = 99
    # pre-enforcement `ser3[4] = 99` interpreted 4 as positional
    ser3[4] = 99
    tm.assert_series_equal(ser3, expected3)

