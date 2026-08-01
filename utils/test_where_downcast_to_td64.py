
def test_where_downcast_to_td64():
    ser = Series([1, 2, 3])

    mask = np.array([False, False, False])

    td = pd.Timedelta(days=1)
    expected = Series([td, td, td], dtype="m8[ns]")

    res2 = ser.where(mask, td)
    expected2 = expected.astype(object)
    tm.assert_series_equal(res2, expected2)

