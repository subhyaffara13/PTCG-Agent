
def test_update_series():
    ser1 = Series([1.0, 2.0, 3.0])
    ser2 = Series([100.0], index=[1])
    ser1_orig = ser1.copy()
    view = ser1[:]

    ser1.update(ser2)

    expected = Series([1.0, 100.0, 3.0])
    tm.assert_series_equal(ser1, expected)
    # ser1 is updated, but its view not
    tm.assert_series_equal(view, ser1_orig)

