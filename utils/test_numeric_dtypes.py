
def test_numeric_dtypes(data, transform_assert_equal):
    transform, assert_equal = transform_assert_equal
    data = transform(data)

    result = to_numeric(data)
    assert_equal(result, data)

