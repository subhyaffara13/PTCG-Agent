
def test_setitem_categorical_assigning_ops():
    orig = Series(Categorical(["b", "b"], categories=["a", "b"]))
    ser = orig.copy()
    ser[:] = "a"
    exp = Series(Categorical(["a", "a"], categories=["a", "b"]))
    tm.assert_series_equal(ser, exp)

    ser = orig.copy()
    ser[1] = "a"
    exp = Series(Categorical(["b", "a"], categories=["a", "b"]))
    tm.assert_series_equal(ser, exp)

    ser = orig.copy()
    ser[ser.index > 0] = "a"
    exp = Series(Categorical(["b", "a"], categories=["a", "b"]))
    tm.assert_series_equal(ser, exp)

    ser = orig.copy()
    ser[[False, True]] = "a"
    exp = Series(Categorical(["b", "a"], categories=["a", "b"]))
    tm.assert_series_equal(ser, exp)

    ser = orig.copy()
    ser.index = ["x", "y"]
    ser["y"] = "a"
    exp = Series(Categorical(["b", "a"], categories=["a", "b"]), index=["x", "y"])
    tm.assert_series_equal(ser, exp)

