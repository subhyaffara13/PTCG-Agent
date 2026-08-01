
def test_setitem_positional_with_casting():
    # GH#45070 case where in __setitem__ we get a KeyError, then when
    #  we fallback we *also* get a ValueError if we try to set inplace.
    # As of 3.0 we always treat int keys as labels, so this becomes
    #  setitem-with-expansion
    ser = Series([1, 2, 3], index=["a", "b", "c"])

    ser[0] = "X"
    expected = Series([1, 2, 3, "X"], index=["a", "b", "c", 0], dtype=object)
    tm.assert_series_equal(ser, expected)

