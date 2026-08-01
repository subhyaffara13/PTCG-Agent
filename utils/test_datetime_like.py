
def test_datetime_like(tz_naive_fixture, transform_assert_equal):
    transform, assert_equal = transform_assert_equal
    idx = pd.date_range("20130101", periods=3, tz=tz_naive_fixture)

    result = to_numeric(transform(idx))
    expected = transform(idx.asi8)
    assert_equal(result, expected)

