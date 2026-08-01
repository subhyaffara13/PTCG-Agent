
def test_raises_empty_input():
    with pytest.raises(ValueError, match="no types given"):
        find_common_type([])

