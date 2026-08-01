
def test_resample_basic_grouper(unit):
    index = date_range("1/1/2000 00:00:00", "1/1/2000 00:13:00", freq="Min")
    s = Series(range(len(index)), index=index)
    s.index.name = "index"
    s.index = s.index.as_unit(unit)
    result = s.resample("5Min").last()
    grouper = Grouper(freq=Minute(5), closed="left", label="left")
    expected = s.groupby(grouper).agg(lambda x: x.iloc[-1])
    tm.assert_series_equal(result, expected)

