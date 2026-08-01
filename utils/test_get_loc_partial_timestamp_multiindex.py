
def test_get_loc_partial_timestamp_multiindex(df):
    mi = df.index
    key = ("2016-01-01", "a")
    loc = mi.get_loc(key)

    expected = np.zeros(len(mi), dtype=bool)
    expected[[0, 3]] = True
    tm.assert_numpy_array_equal(loc, expected)

    key2 = ("2016-01-02", "a")
    loc2 = mi.get_loc(key2)
    expected2 = np.zeros(len(mi), dtype=bool)
    expected2[[6, 9]] = True
    tm.assert_numpy_array_equal(loc2, expected2)

    key3 = ("2016-01", "a")
    loc3 = mi.get_loc(key3)
    expected3 = np.zeros(len(mi), dtype=bool)
    expected3[mi.get_level_values(1).get_loc("a")] = True
    tm.assert_numpy_array_equal(loc3, expected3)

    key4 = ("2016", "a")
    loc4 = mi.get_loc(key4)
    expected4 = expected3
    tm.assert_numpy_array_equal(loc4, expected4)

    # non-monotonic
    taker = np.arange(len(mi), dtype=np.intp)
    taker[::2] = taker[::-2]
    mi2 = mi.take(taker)
    loc5 = mi2.get_loc(key)
    expected5 = np.zeros(len(mi2), dtype=bool)
    expected5[[3, 14]] = True
    tm.assert_numpy_array_equal(loc5, expected5)

