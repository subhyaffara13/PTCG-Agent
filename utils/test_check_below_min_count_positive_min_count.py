
def test_check_below_min_count_positive_min_count(mask, min_count, expected_result):
    # GH35227
    shape = (10, 10)
    result = nanops.check_below_min_count(shape, mask, min_count)
    assert result == expected_result

