
def test_transform_wont_agg_series(string_series, func):
    # GH 35964
    # we are trying to transform with an aggregator
    msg = "Function did not transform"

    with pytest.raises(ValueError, match=msg):
        string_series.transform(func)

