
def test_dt_to_pytimedelta():
    # GH 52284
    data = [timedelta(1, 2, 3), timedelta(1, 2, 4)]
    ser = pd.Series(data, dtype=ArrowDtype(pa.duration("ns")))

    msg = "The behavior of ArrowTemporalProperties.to_pytimedelta is deprecated"
    with tm.assert_produces_warning(Pandas4Warning, match=msg):
        result = ser.dt.to_pytimedelta()
    expected = np.array(data, dtype=object)
    tm.assert_numpy_array_equal(result, expected)
    assert all(type(res) is timedelta for res in result)

    msg = "The behavior of TimedeltaProperties.to_pytimedelta is deprecated"
    with tm.assert_produces_warning(Pandas4Warning, match=msg):
        expected = ser.astype("timedelta64[ns]").dt.to_pytimedelta()
    tm.assert_numpy_array_equal(result, expected)

