
def test_apply_series_on_date_time_index_aware_series(dti, exp, aware):
    # GH 25959
    # Calling apply on a localized time series should not cause an error
    if aware:
        index = dti.tz_localize("UTC").index
    else:
        index = dti.index
    result = Series(index).apply(lambda x: Series([1, 2]))
    tm.assert_frame_equal(result, exp)

