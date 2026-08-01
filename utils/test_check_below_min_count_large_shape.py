
def test_check_below_min_count_large_shape(min_count, expected_result):
    # GH35227 large shape used to show that the issue is fixed
    shape = (2244367, 1253)
    result = nanops.check_below_min_count(shape, mask=None, min_count=min_count)
    assert result == expected_result

