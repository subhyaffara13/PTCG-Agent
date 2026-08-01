
def test_assert_series_equal_identical_na(nulls_fixture):
    ser = Series([nulls_fixture])

    tm.assert_series_equal(ser, ser.copy())

    # while we're here do Index too
    idx = pd.Index(ser)
    tm.assert_index_equal(idx, idx.copy(deep=True))

