
def test_quantile_empty_datetimelike(typ, unit):
    ser = Series([], dtype=f"{typ}[{unit}]")
    result = ser.quantile()
    assert result is pd.NaT


def test_quantile_empty_datetimelike(typ, unit):
    dtype = f"{typ}[{unit}]"
    df = DataFrame(np.array([], dtype=dtype))
    result = df.quantile()
    expected = Series([pd.NaT], name=0.5, dtype=dtype)
    tm.assert_series_equal(result, expected)

