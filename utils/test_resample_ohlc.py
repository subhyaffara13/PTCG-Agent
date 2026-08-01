
def test_resample_ohlc(unit):
    index = date_range(datetime(2005, 1, 1), datetime(2005, 1, 2), freq="Min")
    s = Series(range(len(index)), index=index)
    s.index.name = "index"
    s.index = s.index.as_unit(unit)

    grouper = Grouper(freq=Minute(5))
    expect = s.groupby(grouper).agg(lambda x: x.iloc[-1])
    result = s.resample("5Min").ohlc()

    assert len(result) == len(expect)
    assert len(result.columns) == 4

    xs = result.iloc[-2]
    assert xs["open"] == s.iloc[-6]
    assert xs["high"] == s[-6:-1].max()
    assert xs["low"] == s[-6:-1].min()
    assert xs["close"] == s.iloc[-2]

    xs = result.iloc[0]
    assert xs["open"] == s.iloc[0]
    assert xs["high"] == s[:5].max()
    assert xs["low"] == s[:5].min()
    assert xs["close"] == s.iloc[4]

