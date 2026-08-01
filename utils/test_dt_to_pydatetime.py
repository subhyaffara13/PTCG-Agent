
def test_dt_to_pydatetime():
    # GH 51859
    data = [datetime(2022, 1, 1), datetime(2023, 1, 1)]
    ser = pd.Series(data, dtype=ArrowDtype(pa.timestamp("ns")))
    result = ser.dt.to_pydatetime()
    expected = pd.Series(data, dtype=object)
    tm.assert_series_equal(result, expected)
    assert all(type(expected.iloc[i]) is datetime for i in range(len(expected)))

    expected = ser.astype("datetime64[ns]").dt.to_pydatetime()
    tm.assert_series_equal(result, expected)

