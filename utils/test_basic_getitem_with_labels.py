
def test_basic_getitem_with_labels(datetime_series):
    indices = datetime_series.index[[5, 10, 15]]

    result = datetime_series[indices]
    expected = datetime_series.reindex(indices)
    tm.assert_series_equal(result, expected)

    result = datetime_series[indices[0] : indices[2]]
    expected = datetime_series.loc[indices[0] : indices[2]]
    tm.assert_series_equal(result, expected)

