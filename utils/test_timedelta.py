
def test_timedelta(transform_assert_equal):
    transform, assert_equal = transform_assert_equal
    idx = pd.timedelta_range("1 days", periods=3, freq="D")

    result = to_numeric(transform(idx))
    expected = transform(idx.asi8)
    assert_equal(result, expected)

