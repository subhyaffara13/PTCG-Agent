
def test_resample_anchored_monthstart(simple_date_range_series, freq, unit):
    ts = simple_date_range_series("1/1/2000", "12/31/2002")
    ts.index = ts.index.as_unit(unit)
    ts.resample(freq).mean()

