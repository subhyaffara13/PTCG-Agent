
def test_transform_and_agg_err_series(string_series, func, msg):
    # we are trying to transform with an aggregator
    with pytest.raises(ValueError, match=msg):
        with np.errstate(all="ignore"):
            string_series.agg(func)

