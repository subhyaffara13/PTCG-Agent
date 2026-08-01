
def test_series_invalid_param_combination():
    left = Series(dtype=object)
    right = Series(dtype=object)
    with pytest.raises(
        ValueError, match="check_like must be False if check_index is False"
    ):
        tm.assert_series_equal(left, right, check_index=False, check_like=True)

