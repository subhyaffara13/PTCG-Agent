
def test_resample_ohlc_result(unit):
    # GH 12332
    index = date_range("1-1-2000", "2-15-2000", freq="h").as_unit(unit)
    index = index.union(date_range("4-15-2000", "5-15-2000", freq="h").as_unit(unit))
    s = Series(range(len(index)), index=index)

    a = s.loc[:"4-15-2000"].resample("30min").ohlc()
    assert isinstance(a, DataFrame)

    b = s.loc[:"4-14-2000"].resample("30min").ohlc()
    assert isinstance(b, DataFrame)

