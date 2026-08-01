
def test_getitem_box_float64(datetime_series):
    with pytest.raises(KeyError, match="^5$"):
        datetime_series[5]

