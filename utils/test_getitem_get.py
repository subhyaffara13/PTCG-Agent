
def test_getitem_get(string_series, object_series):
    for obj in [string_series, object_series]:
        idx = obj.index[5]

        assert obj[idx] == obj.get(idx)
        assert obj[idx] == obj.iloc[5]

    # As of 3.0, ints are treated as labels
    assert string_series.get(-1) is None
    assert string_series.iloc[5] == string_series.get(string_series.index[5])

