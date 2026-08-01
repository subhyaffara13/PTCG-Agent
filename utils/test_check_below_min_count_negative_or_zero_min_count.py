
def test_check_below_min_count_negative_or_zero_min_count(min_count):
    # GH35227
    result = nanops.check_below_min_count((21, 37), None, min_count)
    expected_result = False
    assert result == expected_result

