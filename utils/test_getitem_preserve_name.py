
def test_getitem_preserve_name(datetime_series):
    result = datetime_series[datetime_series > 0]
    assert result.name == datetime_series.name

    result = datetime_series[5:10]
    assert result.name == datetime_series.name

