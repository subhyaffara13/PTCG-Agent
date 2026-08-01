
def test_resample_string_kwargs(keyword, value, unit):
    # see gh-19303
    # Check that wrong keyword argument strings raise an error
    index = date_range("1/1/2000 00:00:00", "1/1/2000 00:13:00", freq="Min")
    series = Series(range(len(index)), index=index)
    series.index.name = "index"
    series.index = series.index.as_unit(unit)
    msg = f"Unsupported value {value} for `{keyword}`"
    with pytest.raises(ValueError, match=msg):
        series.resample("5min", **({keyword: value}))

