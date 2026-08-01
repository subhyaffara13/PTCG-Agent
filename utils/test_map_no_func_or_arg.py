
def test_map_no_func_or_arg():
    with pytest.raises(ValueError, match="The `func` parameter is required"):
        Series([1, 2]).map()

