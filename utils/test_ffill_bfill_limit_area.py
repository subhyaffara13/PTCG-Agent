
def test_ffill_bfill_limit_area(data, expected_data, method, kwargs):
    # GH#56492
    s = Series(data)
    expected = Series(expected_data)
    result = getattr(s, method)(**kwargs)
    tm.assert_series_equal(result, expected)


def test_ffill_bfill_limit_area(data, expected_data, method, kwargs):
    # GH#56492
    df = DataFrame(data)
    expected = DataFrame(expected_data)
    result = getattr(df, method)(**kwargs)
    tm.assert_frame_equal(result, expected)

